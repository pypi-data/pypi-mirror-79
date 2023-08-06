import abc
import os
import pickle

import torch
import inflection

from .data import DataNode
from .node import Node
from .optim import OptimNode
from ... import device
from ...writer import ExecWriter


class ExecNode(metaclass=abc.ABCMeta):
    _devices: list
    _writer: ExecWriter

    def __init__(self, root, **kwargs):
        from ..node import NodeIR

        self._nodes = []
        for k, v in kwargs.items():
            if isinstance(v, NodeIR):
                self._nodes.append(k)
            setattr(self, k, v)

        # dump
        with open('dump.pkl', 'wb') as f:
            pickle.dump(self, f)

        self._initialize(root)

    def _initialize(self, root):
        with root.use_exec(self):
            for k, v in self.get_nodes().items():
                setattr(self, k, v.build(root.node_root))

        self._devices = device.parse_device(root.env.devices)
        self._writer = ExecWriter(root.env, self)

    @classmethod
    def load(cls, root, f):
        exec = pickle.load(f)
        exec._initialize(root)
        return exec

    @classmethod
    def link_node(cls, last, new):
        """link the shapes between nodes, such as data->model"""
        from ..node import link_shapes

        link_shapes(last.get_output_shapes(), new.get_input_shapes())

    def get_nodes(self):
        return {k: getattr(self, k) for k in self._nodes}

    def to(self, node):
        # TODO: https://github.com/pytorch/pytorch/blob/master/torch/distributed/launch.py
        # print(self._devices)
        return node.to('cuda:0')

    def get_name(self):
        return self.__class__.__name__


class Trainer(ExecNode, metaclass=abc.ABCMeta):
    data: DataNode
    model: Node

    loss: Node
    optimizer: OptimNode

    epoch: int
    batch_size: int

    def __init__(self, root, data, model, **kwargs):
        self.__class__.link_node(data, model)
        super().__init__(root, data=data, model=model, **kwargs)

    def train(self):
        # Step 1. ready to train
        self._train_begin()

        # Step 2-1. peek the IO
        for epoch, dataset in self._writer.do_epoch('train', self.data.get_train_dataset):
            metrics = {
                'loss': 0.0,
            }
            self._train_epoch_begin(epoch, metrics)

            for idx, data in enumerate(dataset):
                x, y = self._train_iter_begin(data)
                # Step 2-2. clean-up gradients
                self.optimizer.zero_grad()
                # Step 2-3. predict classses
                y_pred = self.model(**x)
                # Step 2-4. calculate difference (loss)
                loss = self.loss(**y_pred, **y)['x']
                # Step 2-5. calculate gradients
                loss.backward()
                # Step 2-6. step
                self.optimizer.step()
                # Step 2-7. store result
                self._train_iter_end(metrics, x, y, y_pred, loss)

            # Step 2-8. store log
            self._train_epoch_end(epoch, metrics)

        # Step 3. clean up
        self._train_end()

    def _train_begin(self):
        self.optimizer.initialize(self.model)
        for name, node in self.get_nodes().items():
            setattr(self, name, self.to(node))

    def _train_epoch_begin(self, epoch, metrics):
        self.model.train()

    def _train_iter_begin(self, data):
        return {'x': self.to(data[0])}, {'y': self.to(data[1])}

    def _train_iter_end(self, metrics, x, y, y_pred, loss):
        metrics['loss'] += loss.item()

    def _train_epoch_end(self, epoch, metrics):
        for name, value in metrics.items():
            epoch.write(name, value, use_batch=True)
        epoch.flush()

    def _train_end(self):
        pass

    @abc.abstractmethod
    def eval(self):
        raise NotImplementedError

    def publish(self, args):
        # Step 1. ready to publish
        self.model.eval()

        # Step 2. get dummy input
        x, _ = next(iter(self.data.get_train_dataset()))

        # Step 3. get parameters
        input_names = ['x']  # 모델의 입력값을 가리키는 이름
        output_names = ['out_x']  # 모델의 출력값을 가리키는 이름
        dynamic_axes = {'x': {0: 'batch_size'},  # 가변적인 길이를 가진 차원
                        'out_x': {0: 'batch_size'}}

        export_params = True  # 모델 파일 안에 학습된 모델 가중치를 저장할지의 여부
        opset_version = 10  # 모델을 변환할 때 사용할 ONNX 버전
        do_constant_folding = True  # 최적하시 상수폴딩을 사용할지의 여부

        name = inflection.underscore(self.model.get_name())
        output_path = os.path.join(args.output_path, f'{name}.onnx')

        # Step 4. export to onnx
        torch.onnx.export(self.model, {'x': x}, output_path,
                          input_names=input_names,
                          output_names=output_names,
                          dynamic_axes=dynamic_axes,

                          export_params=export_params,
                          opset_version=opset_version,
                          do_constant_folding=do_constant_folding,
                          )

        # Step 5. do target-specific publishing
        # TODO: to be implemented
