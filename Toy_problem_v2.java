/*
 * Toy_problem_v2_1.java
 */

import com.comsol.model.*;
import com.comsol.model.util.*;

/** Model exported on May 2 2024, 11:23 by COMSOL 6.2.0.339. */
public class Toy_problem_v2_1 {

  public static Model run() {
    Model model = ModelUtil.create("Model");

    model.modelPath("D:\\Tijs\\Optimization Code\\Toy Problem v2");

    model.label("Toy problem v2.mph");

    model.param().set("P", "300[nm]", "pitch");
    model.param().set("R", "100[nm]", "radius");
    model.param().set("H", "30[nm]", "height np");
    model.param().set("h_air", "600[nm]", "height air");
    model.param().set("h_glass", "600[nm]", "height glass");
    model.param().set("t_pml", "150[nm]", "thickness pml");
    model.param().set("I0", "1[MW/m^2]", "intensity laser");
    model.param().set("lbda", "532[nm]", "wavelength laser");
    model.param().set("power", "I0*P^2", "power laser");
    model.param().set("D", "1[mm]", "laser diameter");
    model.param().set("beam_power", "I0*(0.5*D)^2*pi", "total beam power");
    model.param().set("k", "(1 + 0.045)/2[W/(m*K)]", "average thermal conductivity");
    model.param().set("A", "P*P", "area of unit cell");

    model.component().create("comp1", true);

    model.component("comp1").geom().create("geom1", 3);

    model.component("comp1").label("Component");

    model.result().table().create("tbl1", "Table");

    model.component("comp1").mesh().create("mesh1");

    model.component("comp1").geom("geom1").label("Geometry");
    model.component("comp1").geom("geom1").create("cyl1", "Cylinder");
    model.component("comp1").geom("geom1").feature("cyl1").label("Disc");
    model.component("comp1").geom("geom1").feature("cyl1").set("r", "R");
    model.component("comp1").geom("geom1").feature("cyl1").set("h", "H");
    model.component("comp1").geom("geom1").create("blk1", "Block");
    model.component("comp1").geom("geom1").feature("blk1").label("Top");
    model.component("comp1").geom("geom1").feature("blk1").set("pos", new String[]{"0", "0", "h_air/2"});
    model.component("comp1").geom("geom1").feature("blk1").set("base", "center");
    model.component("comp1").geom("geom1").feature("blk1").set("size", new String[]{"P", "P", "h_air"});
    model.component("comp1").geom("geom1").feature("blk1").set("layername", new String[]{"Layer 1"});
    model.component("comp1").geom("geom1").feature("blk1").set("layer", "t_pml");
    model.component("comp1").geom("geom1").feature("blk1").set("layerbottom", false);
    model.component("comp1").geom("geom1").feature("blk1").set("layertop", true);
    model.component("comp1").geom("geom1").create("blk2", "Block");
    model.component("comp1").geom("geom1").feature("blk2").label("Bottom");
    model.component("comp1").geom("geom1").feature("blk2").set("pos", new String[]{"0", "0", "-h_glass/2"});
    model.component("comp1").geom("geom1").feature("blk2").set("base", "center");
    model.component("comp1").geom("geom1").feature("blk2").set("size", new String[]{"P", "P", "h_glass"});
    model.component("comp1").geom("geom1").feature("blk2").set("layername", new String[]{"Layer 1"});
    model.component("comp1").geom("geom1").feature("blk2").set("layer", "t_pml");
    model.component("comp1").geom("geom1").run();

    model.component("comp1").selection().create("sel1", "Explicit");
    model.component("comp1").selection("sel1").set(5);
    model.component("comp1").selection().create("sel2", "Explicit");
    model.component("comp1").selection("sel2").set(2, 3, 5);
    model.component("comp1").selection().create("adj1", "Adjacent");
    model.component("comp1").selection().create("com1", "Complement");
    model.component("comp1").selection("sel1").label("NP");
    model.component("comp1").selection("sel2").label("PD");
    model.component("comp1").selection("adj1").label("NP-surface");
    model.component("comp1").selection("adj1").set("input", new String[]{"sel1"});
    model.component("comp1").selection("com1").label("PMLD");
    model.component("comp1").selection("com1").set("input", new String[]{"sel2"});

    model.component("comp1").variable().create("var1");
    model.component("comp1").variable("var1")
         .set("nrelPoav", "nx*ewfd.relPoavx+ny*ewfd.relPoavy+nz*ewfd.relPoavz", "Power outflow of the relative fields, time average");
    model.component("comp1").variable("var1").set("sigma_abs", "intop1(ewfd.Qh)/I0", "Absorption cross section");
    model.component("comp1").variable("var1").set("sigma_sc", "intop2(nrelPoav)/I0", "Scattering cross section");
    model.component("comp1").variable("var1").set("sigma_ext", "sigma_sc+sigma_abs", "Extinction cross section");

    model.component("comp1").material().create("mat1", "Common");
    model.component("comp1").material().create("mat2", "Common");
    model.component("comp1").material().create("mat3", "Common");
    model.component("comp1").material("mat1").selection().named("sel1");
    model.component("comp1").material("mat1").propertyGroup().create("RefractiveIndex", "Refractive index");
    model.component("comp1").material("mat2").selection().set(3, 4);
    model.component("comp1").material("mat2").propertyGroup().create("RefractiveIndex", "Refractive index");
    model.component("comp1").material("mat3").selection().set(1, 2);
    model.component("comp1").material("mat3").propertyGroup().create("RefractiveIndex", "Refractive index");

    model.component("comp1").cpl().create("intop1", "Integration");
    model.component("comp1").cpl().create("intop2", "Integration");
    model.component("comp1").cpl("intop1").selection().named("sel1");
    model.component("comp1").cpl("intop2").selection().named("adj1");

    model.component("comp1").coordSystem().create("pml1", "PML");
    model.component("comp1").coordSystem("pml1").selection().named("com1");

    model.component("comp1").physics().create("ewfd", "ElectromagneticWavesFrequencyDomain", "geom1");
    model.component("comp1").physics("ewfd").create("port1", "Port", 2);
    model.component("comp1").physics("ewfd").feature("port1").selection().set(12);
    model.component("comp1").physics("ewfd").feature("port1").create("pportp1", "PeriodicPortReferencePoint", 0);
    model.component("comp1").physics("ewfd").feature("port1").feature("pportp1").selection().set(4);
    model.component("comp1").physics("ewfd").create("port2", "Port", 2);
    model.component("comp1").physics("ewfd").feature("port2").selection().set(6);
    model.component("comp1").physics("ewfd").feature("port2").create("pportp1", "PeriodicPortReferencePoint", 0);
    model.component("comp1").physics("ewfd").feature("port2").feature("pportp1").selection().set(2);
    model.component("comp1").physics("ewfd").create("pc1", "PeriodicCondition", 2);
    model.component("comp1").physics("ewfd").feature("pc1").selection().set(1, 4, 7, 10, 24, 25, 26, 27);
    model.component("comp1").physics("ewfd").create("pc2", "PeriodicCondition", 2);
    model.component("comp1").physics("ewfd").feature("pc2").selection().set(2, 5, 8, 11, 14, 15, 16, 17);
    model.component("comp1").physics("ewfd").create("sctr1", "Scattering", 2);
    model.component("comp1").physics("ewfd").feature("sctr1").selection().set(3, 13);

    model.component("comp1").mesh("mesh1").autoMeshSize(1);

    model.result().table("tbl1").comments("Reflectance (ewfd)");

    model.component("comp1").view("view1").set("transparency", true);

    model.component("comp1").material("mat1").label("Ag");
    model.component("comp1").material("mat1").propertyGroup("def")
         .set("thermalconductivity", new String[]{"429", "0", "0", "0", "429", "0", "0", "0", "429"});
    model.component("comp1").material("mat1").propertyGroup("def").set("density", "10490");
    model.component("comp1").material("mat1").propertyGroup("def").set("heatcapacity", "236");
    model.component("comp1").material("mat1").propertyGroup("RefractiveIndex")
         .set("n", new String[]{"0.054007", "0", "0", "0", "0.054007", "0", "0", "0", "0.054007"});
    model.component("comp1").material("mat1").propertyGroup("RefractiveIndex")
         .set("ki", new String[]{"3.4290", "0", "0", "0", "3.4290", "0", "0", "0", "3.4290"});
    model.component("comp1").material("mat2").label("Air");
    model.component("comp1").material("mat2").propertyGroup("def")
         .set("thermalconductivity", new String[]{"0.045", "0", "0", "0", "0.045", "0", "0", "0", "0.045"});
    model.component("comp1").material("mat2").propertyGroup("def").set("density", "1.293");
    model.component("comp1").material("mat2").propertyGroup("def").set("heatcapacity", "700");
    model.component("comp1").material("mat2").propertyGroup("RefractiveIndex")
         .set("n", new String[]{"1.00027821", "0", "0", "0", "1.00027821", "0", "0", "0", "1.00027821"});
    model.component("comp1").material("mat3").label("Glass");
    model.component("comp1").material("mat3").propertyGroup("def")
         .set("thermalconductivity", new String[]{"1", "0", "0", "0", "1", "0", "0", "0", "1"});
    model.component("comp1").material("mat3").propertyGroup("def").set("density", "2500");
    model.component("comp1").material("mat3").propertyGroup("def").set("heatcapacity", "840");
    model.component("comp1").material("mat3").propertyGroup("RefractiveIndex")
         .set("n", new String[]{"1.5195", "0", "0", "0", "1.5195", "0", "0", "0", "1.5195"});
    model.component("comp1").material("mat3").propertyGroup("RefractiveIndex")
         .set("ki", new String[]{"7.7608 * 10^-9", "0", "0", "0", "7.7608 * 10^-9", "0", "0", "0", "7.7608 * 10^-9"});

    model.component("comp1").physics("ewfd").prop("MeshControl")
         .set("PhysicsControlledMeshMinimumWavelength", "300[nm]");
    model.component("comp1").physics("ewfd").prop("BackgroundField").set("SolveFor", "scatteredField");
    model.component("comp1").physics("ewfd").feature("port1").set("Pin", "power");
    model.component("comp1").physics("ewfd").feature("port1").set("PortSlit", true);
    model.component("comp1").physics("ewfd").feature("port1").set("SlitType", "DomainBacked");
    model.component("comp1").physics("ewfd").feature("port1").set("TogglePowerFlowDirection", 1);
    model.component("comp1").physics("ewfd").feature("port1").set("PortType", "Periodic");
    model.component("comp1").physics("ewfd").feature("port1").set("Eampl", new int[][]{{1}, {0}, {0}});
    model.component("comp1").physics("ewfd").feature("port1").label("Port T");
    model.component("comp1").physics("ewfd").feature("port2").set("PortSlit", true);
    model.component("comp1").physics("ewfd").feature("port2").set("SlitType", "DomainBacked");
    model.component("comp1").physics("ewfd").feature("port2").set("TogglePowerFlowDirection", 1);
    model.component("comp1").physics("ewfd").feature("port2").set("PortType", "Periodic");
    model.component("comp1").physics("ewfd").feature("port2").active(false);
    model.component("comp1").physics("ewfd").feature("port2").label("Port B");
    model.component("comp1").physics("ewfd").feature("pc1").set("PeriodicType", "Floquet");
    model.component("comp1").physics("ewfd").feature("pc1").set("Floquet_source", "FromPeriodicPort");
    model.component("comp1").physics("ewfd").feature("pc1").label("Periodic Condition X");
    model.component("comp1").physics("ewfd").feature("pc2").set("PeriodicType", "Floquet");
    model.component("comp1").physics("ewfd").feature("pc2").set("Floquet_source", "FromPeriodicPort");
    model.component("comp1").physics("ewfd").feature("pc2").label("Periodic Condition Y");

    model.study().create("std1");
    model.study("std1").create("freq", "Frequency");
    model.study("std1").create("stat", "Stationary");

    model.sol().create("sol1");
    model.sol("sol1").study("std1");
    model.sol("sol1").attach("std1");
    model.sol("sol1").create("st1", "StudyStep");
    model.sol("sol1").create("v1", "Variables");
    model.sol("sol1").create("s1", "Stationary");
    model.sol("sol1").feature("s1").create("p1", "Parametric");
    model.sol("sol1").feature("s1").create("fc1", "FullyCoupled");
    model.sol("sol1").feature("s1").create("d1", "Direct");
    model.sol("sol1").feature("s1").create("i1", "Iterative");
    model.sol("sol1").feature("s1").feature("i1").create("mg1", "Multigrid");
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("pr").create("va1", "Vanka");
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("po").create("sv1", "SORVector");
    model.sol("sol1").feature("s1").feature().remove("fcDef");

    model.result().numerical().create("gev1", "EvalGlobal");
    model.result().create("pg1", "PlotGroup3D");
    model.result().create("pg2", "PlotGroup1D");
    model.result("pg1").create("mslc1", "Multislice");
    model.result("pg2").create("plz1", "Polarization");
    model.result("pg2").feature("plz1").create("col1", "Color");
    model.result().export().create("tbl1", "Table");

    model.study("std1").label("Study");
    model.study("std1").feature("freq").set("punit", "Hz");
    model.study("std1").feature("freq").set("plist", "c_const/lbda");
    model.study("std1").feature("stat").active(false);

    model.sol("sol1").attach("std1");
    model.sol("sol1").feature("st1").label("Compile Equations: Frequency Domain");
    model.sol("sol1").feature("v1").label("Dependent Variables 1.1");
    model.sol("sol1").feature("v1").set("clistctrl", new String[]{"p1"});
    model.sol("sol1").feature("v1").set("cname", new String[]{"freq"});
    model.sol("sol1").feature("v1").set("clist", new String[]{"c_const/lbda"});
    model.sol("sol1").feature("s1").label("Stationary Solver 1.1");
    model.sol("sol1").feature("s1").set("stol", 0.01);
    model.sol("sol1").feature("s1").set("probesel", "none");
    model.sol("sol1").feature("s1").feature("dDef").label("Direct 2");
    model.sol("sol1").feature("s1").feature("aDef").label("Advanced 1");
    model.sol("sol1").feature("s1").feature("aDef").set("complexfun", true);
    model.sol("sol1").feature("s1").feature("p1").label("Parametric 1.1");
    model.sol("sol1").feature("s1").feature("p1").set("pname", new String[]{"freq"});
    model.sol("sol1").feature("s1").feature("p1").set("plistarr", new String[]{"c_const/lbda"});
    model.sol("sol1").feature("s1").feature("p1").set("punit", new String[]{"Hz"});
    model.sol("sol1").feature("s1").feature("p1").set("pcontinuationmode", "no");
    model.sol("sol1").feature("s1").feature("fc1").label("Fully Coupled 1.1");
    model.sol("sol1").feature("s1").feature("fc1").set("linsolver", "d1");
    model.sol("sol1").feature("s1").feature("d1").label("Suggested Direct Solver (ewfd)");
    model.sol("sol1").feature("s1").feature("i1").label("Suggested Iterative Solver (ewfd)");
    model.sol("sol1").feature("s1").feature("i1").set("itrestart", 300);
    model.sol("sol1").feature("s1").feature("i1").set("prefuntype", "right");
    model.sol("sol1").feature("s1").feature("i1").feature("ilDef").label("Incomplete LU 1");
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").label("Multigrid 1.1");
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").set("iter", 1);
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("pr").label("Presmoother 1");
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("pr").feature("soDef").label("SOR 1");
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("pr").feature("va1").label("Vanka 1.1");
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("pr").feature("va1").set("iter", 1);
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("pr").feature("va1")
         .set("vankavars", new String[]{"comp1_E"});
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("pr").feature("va1")
         .set("vankasolv", "stored");
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("pr").feature("va1")
         .set("vankarelax", 0.95);
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("po").label("Postsmoother 1");
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("po").feature("soDef").label("SOR 1");
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("po").feature("sv1")
         .label("SOR Vector 1.1");
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("po").feature("sv1").set("iter", 1);
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("po").feature("sv1").set("relax", 0.5);
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("cs").label("Coarse Solver 1");
    model.sol("sol1").feature("s1").feature("i1").feature("mg1").feature("cs").feature("dDef").label("Direct 1");
    model.sol("sol1").runAll();

    model.result().numerical("gev1").label("Reflectance (ewfd)");
    model.result().numerical("gev1").set("table", "tbl1");
    model.result().numerical("gev1")
         .set("expr", new String[]{"sigma_abs", "(sigma_abs*I0*D)/(k*4*A)*(1 - (2*sqrt(A))/(sqrt(pi)*D))", ""});
    model.result().numerical("gev1").set("unit", new String[]{"m^2", "kg^2*m^2/(s^6*K)", ""});
    model.result().numerical("gev1")
         .set("descr", new String[]{"Absorption cross section", "Collective heating at center NP", ""});
    model.result().numerical("gev1").setResult();
    model.result("pg1").label("Electric Field (ewfd)");
    model.result("pg1").set("frametype", "spatial");
    model.result("pg1").feature("mslc1").set("xnumber", "0");
    model.result("pg1").feature("mslc1").set("ynumber", "0");
    model.result("pg1").feature("mslc1").set("multiplanezmethod", "coord");
    model.result("pg1").feature("mslc1").set("zcoord", "5[nm]");
    model.result("pg1").feature("mslc1").set("smooth", "internal");
    model.result("pg1").feature("mslc1").set("resolution", "normal");
    model.result("pg2").label("Polarization Plot (ewfd)");
    model.result("pg2").set("looplevelinput", new String[]{"manual"});
    model.result("pg2").set("titletype", "manual");
    model.result("pg2").set("title", "Polarization states, Color: Phase (Radians)");
    model.result("pg2").set("xlabel", "Jones vector, out-of-plane component");
    model.result("pg2").set("ylabel", "Jones vector, in-plane component");
    model.result("pg2").set("xlabelactive", false);
    model.result("pg2").set("ylabelactive", false);
    model.result("pg2").feature("plz1").set("linewidth", 2);
    model.result("pg2").feature("plz1").set("linewidthslider", 2);
    model.result("pg2").feature("plz1").set("legend", true);
    model.result("pg2").feature("plz1").set("legendmethod", "manual");
    model.result("pg2").feature("plz1").set("legends", new String[]{"Reflection"});

    return model;
  }

  public static void main(String[] args) {
    run();
  }

}
