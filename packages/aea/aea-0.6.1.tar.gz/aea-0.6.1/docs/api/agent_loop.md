<a name="aea.agent_loop"></a>
# aea.agent`_`loop

This module contains the implementation of an agent loop using asyncio.

<a name="aea.agent_loop.BaseAgentLoop"></a>
## BaseAgentLoop Objects

```python
class BaseAgentLoop(WithLogger,  ABC)
```

Base abstract  agent loop class.

<a name="aea.agent_loop.BaseAgentLoop.__init__"></a>
#### `__`init`__`

```python
 | __init__(agent: AbstractAgent, loop: Optional[AbstractEventLoop] = None) -> None
```

Init loop.

:params agent: Agent or AEA to run.
:params loop: optional asyncio event loop. if not specified a new loop will be created.

<a name="aea.agent_loop.BaseAgentLoop.agent"></a>
#### agent

```python
 | @property
 | agent() -> AbstractAgent
```

Get agent.

<a name="aea.agent_loop.BaseAgentLoop.set_loop"></a>
#### set`_`loop

```python
 | set_loop(loop: AbstractEventLoop) -> None
```

Set event loop and all event loopp related objects.

<a name="aea.agent_loop.BaseAgentLoop.start"></a>
#### start

```python
 | start() -> None
```

Start agent loop synchronously in own asyncio loop.

<a name="aea.agent_loop.BaseAgentLoop.setup"></a>
#### setup

```python
 | setup() -> None
```

Set up loop before started.

<a name="aea.agent_loop.BaseAgentLoop.teardown"></a>
#### teardown

```python
 | teardown()
```

Tear down loop on stop.

<a name="aea.agent_loop.BaseAgentLoop.run_loop"></a>
#### run`_`loop

```python
 | async run_loop() -> None
```

Run agent loop.

<a name="aea.agent_loop.BaseAgentLoop.wait_run_loop_stopped"></a>
#### wait`_`run`_`loop`_`stopped

```python
 | async wait_run_loop_stopped() -> None
```

Wait all tasks stopped.

<a name="aea.agent_loop.BaseAgentLoop.stop"></a>
#### stop

```python
 | stop() -> None
```

Stop agent loop.

<a name="aea.agent_loop.BaseAgentLoop.is_running"></a>
#### is`_`running

```python
 | @property
 | is_running() -> bool
```

Get running state of the loop.

<a name="aea.agent_loop.AgentLoopException"></a>
## AgentLoopException Objects

```python
class AgentLoopException(AEAException)
```

Exception for agent loop runtime errors.

<a name="aea.agent_loop.AgentLoopStates"></a>
## AgentLoopStates Objects

```python
class AgentLoopStates(Enum)
```

Internal agent loop states.

<a name="aea.agent_loop.AsyncAgentLoop"></a>
## AsyncAgentLoop Objects

```python
class AsyncAgentLoop(BaseAgentLoop)
```

Asyncio based agent loop suitable only for AEA.

<a name="aea.agent_loop.AsyncAgentLoop.__init__"></a>
#### `__`init`__`

```python
 | __init__(agent: AbstractAgent, loop: AbstractEventLoop = None)
```

Init agent loop.

**Arguments**:

- `agent`: AEA instance
- `loop`: asyncio loop to use. optional

