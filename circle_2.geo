//+
Point(1) = {0, 0, 1.0, 0.005};
//+
Point(2) = {2.2, 0, 1, 0.005};
//+
Point(3) = {2.2, 0.41, 1, 0.005};
//+
Point(4) = {0, 0.41, 1, 0.005};
//+
Point(5) = {0.2, 0.2, 1, 0.005};
//+
Point(6) = {0.25, 0.2, 1, 0.005};
//+
Point(7) = {0.2, 0.15, 1, 0.005};
//+
Point(8) = {0.15, 0.2, 1, 0.005};
//+
Point(9) = {0.2, 0.25, 1, 0.005};
//+
Circle(1) = {6, 5, 9};
//+
Circle(2) = {6, 5, 7};
//+
Circle(3) = {7, 5, 8};
//+
Circle(4) = {8, 5, 9};
//+
Line(5) = {4, 3};
//+
Line(6) = {3, 2};
//+
Line(7) = {2, 1};
//+
Line(8) = {1, 4};
//+
Curve Loop(1) = {5, 6, 7, 8};
//+
Curve Loop(2) = {1, -4, -3, -2};
//+
Plane Surface(1) = {1, 2};

Extrude {0, 0, 0.1} {
  Surface{1};
  Layers{1};
  Recombine;
}

Physical Surface("In", 51) = {33};
//+
Physical Surface("Out", 52) = {25};
//+
Physical Surface("Bottom", 53) = {29};
//+
Physical Surface("Top", 54) = {21};
//+
Physical Surface("Circle", 55) = {49, 45, 41, 37};
//+
Physical Surface("FrontBack", 56) = {50, 1};
//+
Physical Volume("Volume", 57) = {1};
