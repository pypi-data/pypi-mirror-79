# -*- coding: utf-8 -*-

# Copyright 2014 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import

from sydent.replication.peer import RemotePeer


class PeerStore:
    def __init__(self, sydent):
        self.sydent = sydent

    def getPeerByName(self, name):
        """
        Retrieves a remote peer using it's server name.

        :param name: The server name of the peer.
        :type name: unicode

        :return: The retrieved peer.
        :rtype: RemotePeer
        """
        cur = self.sydent.db.cursor()
        res = cur.execute("select p.name, p.port, p.lastSentVersion, pk.alg, pk.key from peers p, peer_pubkeys pk "
                          "where p.name = ? and pk.peername = p.name and p.active = 1", (name,))

        serverName = None
        port = None
        lastSentVer = None
        pubkeys = {}

        for row in res.fetchall():
            serverName = row[0]
            port = row[1]
            lastSentVer = row[2]
            pubkeys[row[3]] = row[4]

        if len(pubkeys) == 0:
            return None

        p = RemotePeer(self.sydent, serverName, port, pubkeys, lastSentVer)

        return p

    def getAllPeers(self):
        """
        Retrieve all of the remote peers from the database.

        :return: A list of the remote peers this server knows about.
        :rtype: list[RemotePeer]
        """
        cur = self.sydent.db.cursor()
        res = cur.execute("select p.name, p.port, p.lastSentVersion, pk.alg, pk.key from peers p, peer_pubkeys pk "
                          "where pk.peername = p.name and p.active = 1")

        peers = []

        peername = None
        port = None
        lastSentVer = None
        pubkeys = {}

        for row in res.fetchall():
            if row[0] != peername:
                if len(pubkeys) > 0:
                    p = RemotePeer(self.sydent, peername, port, pubkeys, lastSentVer)
                    peers.append(p)
                    pubkeys = {}
                peername = row[0]
                port = row[1]
                lastSentVer = row[2]
            pubkeys[row[3]] = row[4]

        if len(pubkeys) > 0:
            p = RemotePeer(self.sydent, peername, port, pubkeys, lastSentVer)
            peers.append(p)

        return peers

    def setLastSentVersionAndPokeSucceeded(self, peerName, lastSentVersion, lastPokeSucceeded):
        """
        Sets the ID of the last association sent to a given peer and the time of the
        last successful request sent to that peer.

        :param peerName: The server name of the peer.
        :type peerName: unicode
        :param lastSentVersion: The ID of the last association sent to that peer.
        :type lastSentVersion: int
        :param lastPokeSucceeded: The timestamp in milliseconds of the last successful
            request sent to that peer.
        :type lastPokeSucceeded: int
        """
        cur = self.sydent.db.cursor()
        cur.execute("update peers set lastSentVersion = ?, lastPokeSucceededAt = ? "
                          "where name = ?", (lastSentVersion, lastPokeSucceeded, peerName))
        self.sydent.db.commit()
