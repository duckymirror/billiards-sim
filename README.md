# billiards-sim
 A quick and unrealistic simulation of a billiard table
## The configuration file
The scenario that should be simulated can be configured in a YAML file. You can specify this file as `python -m billiards_sim config.yaml`. An example can be found in [`example_config.yaml`](example_config.yaml).

The following options exist:

### `fps`
_Optional, default: `60`_

This configures the frames rendered each second. A higher value makes the animation look smoother and increases the simulation accuracy.

### `tpf`
_Optional, default: `10`_

This option sets the number of simulation steps that are calculated for each animation frame. An increase in this value can be used to compensate for a decrease in `fps`.

### `width`
_Optional, default: `1270`_

Table width in mm.

### `height`
_Optional, default: `2540`_

Table length in mm.

### `radius`
_Optional, default: `28.6`_

Ball radius in mm.

### `invert_y`
_Optional, default: `true`_

When true, inverts the y axis so that (0|0) is in the bottom left corner.

### `paused`
_Optional, default: `false`_

When true, the simulation starts paused. Press space to unpause.

### `friction`
_Optional, default: `0`_

The friction of the balls on the table in mm/s².

### `pockets`
_Optional, default: empty_

This option contains a list of pockets that should be added to the table. The following options can be used to define a pocket:

#### `side`
_Required_

Defines on which side (`top`, `left`, `bottom`, `right`) or corner (`top_left`, `top_right`, `bottom_left`, `bottom_right`) of the table the pocket should be positioned.

#### `pos`
_Required if `side` doesn't specify a corner, otherwise not allowed_

Used to position the pocket. Specifies the distance in mm from the 0 coordinate on this side.

#### `diameter`
_Required_

The distance between the two ends of the pocket.

### `balls`
_Optional, default: empty_

This option contains a list of balls the simulation starts with. The following options can be used to define a ball:

#### `name`
_Optional, default: none_

A ball's name can be used to define actions involving this ball.

#### `color`
_Required_

An array that specifies the RGB color value of the ball.

#### `stripe`
_Optional, default: `false`_

When `true`, the specified color is used as the color of a stripe on white background.

#### `pos`
_Required_

Specifies the initial coordinates of the ball.

#### `vel`
_Required_

Specifies the initial velocity of the ball.

### `actions`
_Optional, default: empty_

This option contains a sequence of actions that should be executed in the simulation. An action ends when all balls have stopped moving. Each action is defined by the name of the ball to apply it to and exactly one action type. The following options are possible:

#### `ball`
_Required_

The name of the ball that should be used when performing the action.

#### `vel`
_Action type, only one per action_

This action sets the ball's velocity to the given value.

#### `push`
_Action type, only one per action_

Use this action to push a ball to a destination by hitting it with another ball. The following options are available:

##### `ball`
_Required_

The name of the ball that should be hit and pushed to the destination.

##### `dest`
_Required_

The destination the pushed ball should move towards.

##### `vel`
_Required_

The absolute velocity the pushing ball should be hit with.

##### `rail`
_Optional, default: none_

The pushing ball can be moved so that it bounces off a rail before hitting the target ball. This option is used to specify which rail is to be used (`top`, `left`, `bottom`, `right`). When set to `auto`, the simulator decides whether a rail should be used and which rail is optimal, ignoring any balls in the way.
