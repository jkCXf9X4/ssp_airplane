within Aircraft;
model AdaptiveWingSystem
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real referenceArea = 28 "m2";
  parameter Real span = 10 "m";
  parameter Real wingAreaScale(min=0.7, max=1.3) = 1.0;
  parameter Real aspectRatio = 3.6;
  parameter Real liftCoeffBase = 0.75;
  input GI.SurfaceActuationCommand controlSurfaces "structured command from mission computer";
  output GI.LiftState liftInterface;
protected
  Real liftCommand;
equation
  liftCommand = (controlSurfaces.left_aileron_deg - controlSurfaces.right_aileron_deg) / 18
              + controlSurfaces.elevator_deg / 12;
  liftInterface.lift_kn = liftCoeffBase * wingAreaScale * (1 + liftCommand);
  liftInterface.drag_kn = 0.12 * liftInterface.lift_kn;
  liftInterface.pitching_moment_knm = controlSurfaces.elevator_deg * referenceArea / aspectRatio;
end AdaptiveWingSystem;
