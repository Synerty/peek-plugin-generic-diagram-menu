from typing import Union

from twisted.internet.defer import Deferred
from vortex.Payload import Payload
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TuplesProviderABC

from peek_plugin_generic_diagram_menu._private.storage.GenericDiagramMenuTuple import \
    GenericDiagramMenuTuple

import logging
from vortex.DeferUtil import deferToThreadWrapWithLogger

logger = logging.getLogger(__name__)

class GenericDiagramMenuTupleProvider(TuplesProviderABC):
    def __init__(self, ormSessionCreator):
        self._ormSessionCreator = ormSessionCreator

    @deferToThreadWrapWithLogger(logger)
    def makeVortexMsg(self, filt: dict,
                      tupleSelector: TupleSelector) -> Union[Deferred, bytes]:

        session = self._ormSessionCreator()
        try:
            tuples = session.query(GenericDiagramMenuTuple).all()

            # Create the vortex message
            return Payload(filt, tuples=tuples).makePayloadEnvelope().toVortexMsg()

        finally:
            session.close()
