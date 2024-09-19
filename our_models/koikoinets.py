# -*- coding: utf-8 -*-
"""
improved by KateSawada
"""
from __future__ import annotations
from typing import Any, Type

import torch  # 1.8.1
import torch.nn as nn
import torch.nn.functional as F

# length: 48(discard/pick), 50(koikoi)
# origin input size: (BATCH_SIZE, nFeature, length)
# conv1d input size: (BATCH_SIZE, nFeature, length)
# multiheadattention input size: (length, BATCH_SIZE, nFeature)

# %%
NetParameter = {"nInput": 300, "nEmb": 256, "nFw": 512, "nAttnHead": 4, "nLayer": 2}


def load_models() -> tuple[KoiKoiModelBase, KoiKoiModelBase, KoiKoiModelBase]:
    """モデルを読み込む関数

    Returns:
        tuple[KoiKoiModelBase, KoiKoiModelBase, KoiKoiModelBase]: 順番に，Discard, Pick, Koikoi
    """
    return DiscardModel(), PickModel(), KoiKoiModel()


class KoiKoiModelBase(nn.Module):
    def __init__(self):
        super(KoiKoiModelBase, self).__init__()

def decide_action(self, x: torch.Tensor, legal_actions: list) -> Any:
        """モデルの出力に基づいて行動をひとつ選ぶ

        Args:
            x (torch.Tensor): モデルの
            legal_actions (list): observation.legal_actions

        Returns:
            Any: _description_
        """
        return legal_actions[0]

class KoiKoiEncoderBlock(nn.Module):
    def __init__(self, nInput, nEmb, nFw, nAttnHead, nLayer):
        super(KoiKoiEncoderBlock, self).__init__()
        self.f1 = nn.Conv1d(nInput, nFw, 1)
        self.f2 = nn.Conv1d(nFw, nEmb, 1)
        attn_layer = nn.TransformerEncoderLayer(nEmb, nAttnHead, nFw)
        self.attn_encoder = nn.TransformerEncoder(attn_layer, nLayer)

    def forward(self, x):
        x = self.f2(F.relu(self.f1(x)))
        x = F.layer_norm(x, [x.size(-1)])
        x = x.permute(2, 0, 1)
        x = self.attn_encoder(x)
        x = x.permute(1, 2, 0)
        return x

class DiscardModel(KoiKoiModelBase):
    def __init__(self):
        super(DiscardModel, self).__init__()
        self.encoder_block = KoiKoiEncoderBlock(**NetParameter)
        self.out = nn.Conv1d(NetParameter["nEmb"], 1, 1)

    def forward(self, x):
        x = self.encoder_block(x)
        x = self.out(x).squeeze(1)
        return x


class PickModel(KoiKoiModelBase):
    def __init__(self):
        super(PickModel, self).__init__()
        self.encoder_block = KoiKoiEncoderBlock(**NetParameter)
        self.out = nn.Conv1d(NetParameter["nEmb"], 1, 1)

    def forward(self, x):
        x = self.encoder_block(x)
        x = self.out(x).squeeze(1)
        return x


class KoiKoiModel(KoiKoiModelBase):
    def __init__(self):
        super(KoiKoiModel, self).__init__()
        self.encoder_block = KoiKoiEncoderBlock(**NetParameter)
        self.out = nn.Conv1d(NetParameter["nEmb"], 1, 1)

    def forward(self, x):
        x = self.encoder_block(x)
        x = self.out(x[:, :, [0, 1]]).squeeze(1)
        return x


class TargetQNet(nn.Module):
    def __init__(self):
        super(TargetQNet, self).__init__()
        self.encoder_block = KoiKoiEncoderBlock(**NetParameter)
        self.out = nn.Conv1d(NetParameter["nEmb"], 1, 1)

    def forward(self, x):
        x = self.encoder_block(x)
        x = self.out(x[:, :, 0].unsqueeze(2)).squeeze(1)
        return x
