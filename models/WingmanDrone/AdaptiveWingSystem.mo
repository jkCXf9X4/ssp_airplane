within WingmanDrone;
model AdaptiveWingSystem
  import GI = WingmanDrone.GeneratedInterfaces;
  parameter Real referenceArea = 28 "m2";
  parameter Real span = 7.3 "m";
  parameter Real wingAreaScale(min=0.7, max=1.3) = 1.0;
  parameter Real aspectRatio = 5.5;
  input GI.SurfaceActuationCommand controlSurfaces "structured command from mission computer";
  output GI.LiftState liftInterface;
protected
  parameter Real baseLiftCoeff = 0.6;
  Real liftCommand;
equation
  liftCommand = (controlSurfaces.left_aileron_deg - controlSurfaces.right_aileron_deg) / 20
              + controlSurfaces.elevator_deg / 15;
  liftInterface.lift_kn = baseLiftCoeff * wingAreaScale * (1 + liftCommand);
  liftInterface.drag_kn = 0.1 * liftInterface.lift_kn;
  liftInterface.pitching_moment_knm = controlSurfaces.elevator_deg * referenceArea / aspectRatio;
end AdaptiveWingSystem;
