class PauseResumeMixin(object):

    def __init__(self):
        super().__init__()
        self._prev_state = None

    @property
    def state(self):
        return self._state

    def pause(self):

        if not self.is_pause():
            self._set_pause()
            self._do_pause()

        return self.state

    def resume(self):
        if self.is_pause():
            self._set_resume()
            self._do_resume()

        return self.state

    def is_pause(self):
        from .stream import StreamState

        return self.state == StreamState.Pause

    def _set_pause(self):
        from .stream import StreamState

        self._prev_state = self.state
        self._state = StreamState.Pause

    def _set_resume(self):
        self._state = self._prev_state

    def _do_pause(self):
        # for override
        pass

    def _do_resume(self):
        # for override
        pass
