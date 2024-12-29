//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {15, 10, 0, 1.0};
//+
Point(3) = {15, 0, 0, 1.0};
//+
Point(4) = {0, 10, 0, 1.0};
//+
Line(1) = {1, 3};
//+
Line(2) = {3, 2};
//+
Line(3) = {2, 4};
//+
Line(4) = {4, 1};
//+
Point(5) = {2, 5, 0, 0.1};
//+
Point(6) = {2, 4.5, 0, 0.1};
//+
Point(7) = {2, 5.5, 0, 0.1};
//+
Point(8) = {2.5, 5, 0, 0.1};
//+
Point(9) = {1.5, 5, 0, 0.1};
//+
Circle(5) = {6, 5, 9};
//+
Circle(6) = {9, 5, 7};
//+
Circle(7) = {7, 5, 8};
//+
Circle(8) = {8, 5, 6};
//+
Curve Loop(1) = {3, 4, 1, 2};
//+
Curve Loop(2) = {7, 8, 5, 6};
//+
Plane Surface(1) = {1, 2};
//+
Extrude {0, 0, 1} {
  Surface{1};
  Layers{1};
  Recombine;
}
//+
Physical Surface("In", 51) = {25};
//+
Physical Surface("Out", 52) = {33};
//+
Physical Surface("Bottom", 53) = {29};
//+
Physical Surface("Top", 54) = {21};
//+
Physical Surface("Circle", 55) = {49, 45, 41, 37};
//+
Physical Surface("FrontBack", 56) = {1, 50};
//+
Physical Volume("Volume", 57) = {1};
//+
Physical Volume("Volume", 57) += {1};
