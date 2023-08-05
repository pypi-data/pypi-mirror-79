#!/usr/bin/python
"""
    Copyright (c) 2016-present,
    Jaguar0625, gimre, BloodyRookie, Tech Bureau, Corp. All rights reserved.

    This file is part of Catapult.

    Catapult is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Catapult is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Catapult. If not, see <http://www.gnu.org/licenses/>.
"""

# pylint: disable=W0622,W0612,C0301,R0904

from __future__ import annotations
from .GeneratorUtils import GeneratorUtils
from .FinalizationPointDto import FinalizationPointDto
from .LinkActionDto import LinkActionDto
from .VotingKeyDto import VotingKeyDto


class VotingKeyLinkTransactionBodyBuilder:
    """Binary layout for a voting key link transaction.

    Attributes:
        linkedPublicKey: Linked public key.
        startPoint: Start finalization point.
        endPoint: End finalization point.
        linkAction: Link action.
    """

    def __init__(self, linkedPublicKey: VotingKeyDto, startPoint: FinalizationPointDto, endPoint: FinalizationPointDto, linkAction: LinkActionDto):
        """Constructor.
        Args:
            linkedPublicKey: Linked public key.
            startPoint: Start finalization point.
            endPoint: End finalization point.
            linkAction: Link action.
        """
        self.linkedPublicKey = linkedPublicKey
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.linkAction = linkAction

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> VotingKeyLinkTransactionBodyBuilder:
        """Creates an instance of VotingKeyLinkTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of VotingKeyLinkTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        linkedPublicKey = VotingKeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[linkedPublicKey.getSize():]
        startPoint = FinalizationPointDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[startPoint.getSize():]
        endPoint = FinalizationPointDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[endPoint.getSize():]
        linkAction = LinkActionDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[linkAction.getSize():]
        return VotingKeyLinkTransactionBodyBuilder(linkedPublicKey, startPoint, endPoint, linkAction)

    def getLinkedPublicKey(self) -> VotingKeyDto:
        """Gets linked public key.
        Returns:
            Linked public key.
        """
        return self.linkedPublicKey

    def getStartPoint(self) -> FinalizationPointDto:
        """Gets start finalization point.
        Returns:
            Start finalization point.
        """
        return self.startPoint

    def getEndPoint(self) -> FinalizationPointDto:
        """Gets end finalization point.
        Returns:
            End finalization point.
        """
        return self.endPoint

    def getLinkAction(self) -> LinkActionDto:
        """Gets link action.
        Returns:
            Link action.
        """
        return self.linkAction

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.linkedPublicKey.getSize()
        size += self.startPoint.getSize()
        size += self.endPoint.getSize()
        size += self.linkAction.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.linkedPublicKey.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.startPoint.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.endPoint.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.linkAction.serialize())  # kind:CUSTOM
        return bytes_
