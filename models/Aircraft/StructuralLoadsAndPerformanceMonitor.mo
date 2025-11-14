within Aircraft;
model StructuralLoadsAndPerformanceMonitor
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real maxLoadFactor_g = 9;
  parameter Real maxMach = 2.0;
  parameter Real releaseInhibit_g = 5.5;
  input GI.LiftState liftIn;
  input GI.ThrustState thrustIn;
  input GI.AirDataInertialState airDataIn;
  output GI.StructuralPerformanceState performanceStatus;
protected
  Real estimatedLoad;
  Real margin;
equation
  estimatedLoad = min(maxLoadFactor_g, max(1.0, liftIn.lift_kn / max(5.0, thrustIn.thrust_kn + 1)));
  margin = max(0.0, 1 - estimatedLoad / maxLoadFactor_g);

  performanceStatus.load_factor_g = estimatedLoad;
  performanceStatus.mach_estimate = max(0, airDataIn.mach_number);
  performanceStatus.structural_margin_norm = margin;
  performanceStatus.stores_release_inhibit = estimatedLoad > releaseInhibit_g or airDataIn.mach_number > 0.9 * maxMach;
  performanceStatus.autopilot_limit_code = if performanceStatus.stores_release_inhibit then 2 else 0;
end StructuralLoadsAndPerformanceMonitor;
