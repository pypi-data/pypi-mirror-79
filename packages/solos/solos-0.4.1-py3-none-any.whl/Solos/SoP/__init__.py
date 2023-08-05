import os
from random import randint
from functools import partial

import torch
from torchvision.utils import make_grid
import numpy as np

from flerken.framework.framework import Trainer
from flerken.framework.meters import TensorStorage, TensorHandler, get_nested_meter
from flerken.utils.losses import SI_SDR
from flerken.utils import BaseDict

from .config import transforms
from .config.deep_config import AUDIO_FRAMERATE
from .models import get_network
from . import utils, config
from .utils.dataset import get_dataset
from .. import get_solos_timestamps

SOP_PATH = __path__[0]


class Trainer(Trainer):
    def hook(self, vrs):
        json_path = os.path.join(self.results_path[self.state], str(self.epoch))
        #
        # if not os.path.exists(json_path):
        #     os.mkdir(json_path)
        # json_path = os.path.join(json_path)
        # json_path = os.path.join(json_path, f'{self.epoch}it_{self.absolute_iter}.json')
        # gt = (torch.sigmoid(vrs['pred'][:, 0, ...]) > 0.5).cpu().numpy().astype(np.int8)
        # if self.state == 'train':
        #     trace = {i: x for i, x in enumerate(vrs['vs']['trace'])}
        # else:
        #     trace = {i: x.trace for i, x in enumerate(vrs['vs']['trace'])}
        # trace = BaseDict(trace)
        # for key in trace:
        #     trace[key]['pred'] = gt[key].tolist()
        # trace.write(json_path)

    def init_metrics(self):
        self.init_loss()
        self.metrics['sdr'] = get_sdr_meter()
        self.set_tensor_scalar_item('sdr')


def get_sdr_meter():
    f = SI_SDR()
    handler = TensorHandler('detach', 'istft', 'lin_freq_batch', **transforms)

    def func(pred, gt, vs):
        pred_sp = torch.view_as_real(pred.squeeze(1) * vs['spm_with_phase'])
        audio = handler(pred_sp)
        audio_gt = vs['ad1']
        sdr = f(audio, audio_gt)
        return sdr

    def func2(pred, gt, vs):
        pred_sp = torch.view_as_real(gt.squeeze(1) * vs['spm_with_phase'])
        audio = handler(pred_sp)
        audio_gt = vs['ad1']
        sdr = f(audio, audio_gt)
        return sdr

    def func3(pred, gt, vs):
        pred_sp = torch.view_as_real((pred.squeeze(1) * vs['spm_with_phase']))
        gt_sp = torch.view_as_real((gt.squeeze(1) * vs['spm_with_phase']))
        audio = handler(pred_sp)
        audio_gt = handler(gt_sp)
        sdr = f(audio_gt, audio)
        return sdr

    handlers = {}
    handlers['gt'] = TensorHandler('detach', 'to_cpu', **transforms)
    handlers['pred'] = TensorHandler('detach', 'to_cpu', 'sigmoid', **transforms)
    # handlers['sdr'] = func
    handlers['vs'] = lambda x: x
    # handlers['oracle'] = func2
    handlers['sdr_oracle'] = func3
    opt = {'gt': {'type': 'input', 'store': 'list'},
           'pred': {'type': 'input', 'store': 'list'},
           'vs': {'type': 'input', 'store': 'list'},
           # 'sdr': {'type': 'output', 'store': 'list'},
           # 'oracle': {'type': 'output', 'store': 'list'},
           'sdr_oracle': {'type': 'output', 'store': 'list'}
           }
    return get_nested_meter(
        partial(TensorStorage, handlers=handlers, opt=opt, on_the_fly=True,
                # redirect={'sdr': 'sdr', 'oracle': 'oracle', 'sdr_oracle': 'sdr'}), 1)
                redirect={'sdr_oracle': 'sdr'}), 1)
