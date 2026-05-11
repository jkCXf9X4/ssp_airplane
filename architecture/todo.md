
Fix the sysml formatting to align with standard

1. Import scalar values
 - private import ScalarValues::*;

2. Set all attributes type

3. move attribute comments and docs into its proper scope:
example:
attribute throttle_norm : Real {
    /* Test comment */
    doc /* Test documentation */
}

4. Make import more correct:

Divide files by subpackages:
Example
package Aircraft::Interfaces {

In higher levels import:
example
package Aircraft::Subsystems {
  import ScalarValues::*;
  import Aircraft::Interfaces::*;



To do later...

Fix arrays, 
example:

import Collections::*;

attribute waypointX_km : Array<Real> = (0.0, 10.0, 20.0);

Way later....
or even more sysml-ish:

attribute def Waypoint {
    attribute x_km : Real;
    attribute y_km : Real;
    attribute z_km : Real;
}

attribute waypoints : Waypoint[3];

attribute wp0 : Waypoint {
    :>> x_km = 0.0;
    :>> y_km = 0.0;
    :>> z_km = 5.0;
}