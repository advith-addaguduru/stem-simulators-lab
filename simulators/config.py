"""
STEM Lab — Simulator Catalog
=============================
Maps Pack → Subject → Topics.
Each topic entry: name, icon, desc, detail, refs, module path, function name.
"""

CATALOG = {
    # ── Foundation Pack ───────────────────────────────────────────────────────
    "📦 Foundation (Grades 6–8)": {
        "icon": "🔰",
        "desc": "Build core STEM foundations — motion, circuits, matter, light, sound, and geometry.",
        "subjects": {
            "🔬 Physics": [
                {
                    "name": "Forces & Motion Basics",
                    "icon": "🚀",
                    "desc": "How forces make things move, stop, and change direction",
                    "detail": (
                        "Explore the relationship between speed, distance, and time "
                        "using the formula speed = distance ÷ time. Investigate "
                        "Newton's Second Law (F = ma) to see how force and mass "
                        "affect acceleration, and discover how friction opposes "
                        "motion on different surfaces."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Forces and Newton's Laws", "url": "https://www.khanacademy.org/science/physics/forces-newtons-laws"},
                        {"title": "BBC Bitesize — Forces", "url": "https://www.bbc.co.uk/bitesize/topics/zf66fg8"},
                        {"title": "PhET — Forces and Motion: Basics", "url": "https://phet.colorado.edu/en/simulations/forces-and-motion-basics"},
                    ],
                    "module": "simulators.physics.lower_secondary.forces_and_motion",
                    "func": "simulate",
                },
                {
                    "name": "Simple Circuits",
                    "icon": "💡",
                    "desc": "Build circuits with batteries, bulbs, and resistors",
                    "detail": (
                        "Explore Ohm's law (V = IR) by building a simple battery-and-bulb "
                        "circuit and observing how voltage, current, and resistance "
                        "interact. Compare conductors vs insulators by their "
                        "resistivity, and wire series and parallel circuits to see "
                        "how total resistance and brightness change."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Introduction to Circuits", "url": "https://www.khanacademy.org/science/physics/circuits-topic"},
                        {"title": "BBC Bitesize — Electric Circuits", "url": "https://www.bbc.co.uk/bitesize/topics/zq99q6f"},
                        {"title": "PhET — Circuit Construction Kit: DC", "url": "https://phet.colorado.edu/en/simulations/circuit-construction-kit-dc"},
                    ],
                    "module": "simulators.physics.lower_secondary.simple_circuits",
                    "func": "simulate",
                },
                {
                    "name": "Energy Transfers & Forces",
                    "icon": "⚡",
                    "desc": "How energy moves between objects and changes form",
                    "detail": (
                        "Calculate kinetic and potential energy and observe real-time "
                        "conversions between them. Simulate a ball drop to explore "
                        "energy conservation, and model heating and cooling curves "
                        "using Newton's law of cooling."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Work and Energy", "url": "https://www.khanacademy.org/science/physics/work-and-energy"},
                        {"title": "BBC Bitesize — Energy Transfers", "url": "https://www.bbc.co.uk/bitesize/topics/zc3g87h"},
                        {"title": "PhET — Energy Skate Park", "url": "https://phet.colorado.edu/en/simulations/energy-skate-park-basics"},
                    ],
                    "module": "simulators.physics.lower_secondary.energy_transfers",
                    "func": "simulate",
                },
                {
                    "name": "Magnets & Magnetic Fields",
                    "icon": "🧲",
                    "desc": "Explore magnetic field lines, compasses & electromagnets",
                    "detail": (
                        "Visualise the magnetic field of a bar-magnet dipole using "
                        "field-line plots produced with matplotlib streamplot. "
                        "Place a compass needle at any point to see the field "
                        "direction, and investigate how current and number of turns "
                        "affect electromagnet strength (B = μ₀NI/L)."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Magnets and Magnetic Force", "url": "https://www.khanacademy.org/science/physics/magnetic-forces-and-magnetic-fields"},
                        {"title": "BBC Bitesize — Magnetism", "url": "https://www.bbc.co.uk/bitesize/topics/zf66fg8/articles/znkqpg8"},
                        {"title": "PhET — Magnets and Electromagnets", "url": "https://phet.colorado.edu/en/simulations/magnets-and-electromagnets"},
                    ],
                    "module": "simulators.physics.lower_secondary.magnets",
                    "func": "simulate",
                },
                {
                    "name": "Light & Sound Waves",
                    "icon": "🌊",
                    "desc": "How light reflects and refracts, and how sound travels",
                    "detail": (
                        "Simulate the law of reflection (angle of incidence = angle "
                        "of reflection), apply Snell's law to model refraction "
                        "between media, and visualise transverse sound waves with "
                        "adjustable frequency and amplitude."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Light", "url": "https://www.khanacademy.org/science/physics/geometric-optics"},
                        {"title": "BBC Bitesize — Light and Sound", "url": "https://www.bbc.co.uk/bitesize/topics/zq2mn39"},
                        {"title": "PhET — Bending Light", "url": "https://phet.colorado.edu/en/simulations/bending-light"},
                    ],
                    "module": "simulators.physics.lower_secondary.light_and_sound",
                    "func": "simulate",
                },
            ],
            "⚗️ Chemistry": [
                {
                    "name": "States of Matter",
                    "icon": "🧊",
                    "desc": "How temperature changes solids, liquids, and gases",
                    "detail": (
                        "Visualise the particle model for solids, liquids, and gases "
                        "and see how particles behave at different temperatures. "
                        "Trace a full heating curve from ice through water to steam "
                        "and compare densities of common substances."
                    ),
                    "refs": [
                        {"title": "Khan Academy — States of Matter", "url": "https://www.khanacademy.org/science/chemistry/states-of-matter-and-intermolecular-forces"},
                        {"title": "BBC Bitesize — States of Matter", "url": "https://www.bbc.co.uk/bitesize/topics/zkgg87h"},
                        {"title": "PhET — States of Matter", "url": "https://phet.colorado.edu/en/simulations/states-of-matter-basics"},
                    ],
                    "module": "simulators.chemistry.lower_secondary.states_of_matter",
                    "func": "simulate",
                },
                {
                    "name": "Elements & Compounds",
                    "icon": "🔬",
                    "desc": "Atoms, elements, and how they combine into compounds",
                    "detail": (
                        "Browse the first 20 elements of the periodic table with "
                        "interactive info cards. Learn the difference between "
                        "elements, compounds, and mixtures, and practise balancing "
                        "simple word equations."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Atoms, Compounds and Ions", "url": "https://www.khanacademy.org/science/chemistry/atomic-structure-and-properties"},
                        {"title": "BBC Bitesize — Elements and Compounds", "url": "https://www.bbc.co.uk/bitesize/topics/zsycd6f"},
                        {"title": "PhET — Build an Atom", "url": "https://phet.colorado.edu/en/simulations/build-an-atom"},
                    ],
                    "module": "simulators.chemistry.lower_secondary.elements_and_compounds",
                    "func": "simulate",
                },
                {
                    "name": "Separation Techniques",
                    "icon": "🔬",
                    "desc": "Filtration, distillation & chromatography",
                    "detail": (
                        "Simulate three key separation techniques: filtration "
                        "(split a mixture by particle size and view a pie chart "
                        "of collected vs residue mass), evaporation & distillation "
                        "(compare boiling points and trace a heating curve), and "
                        "chromatography (set Rf values for up to five dyes and "
                        "visualise the chromatogram)."
                    ),
                    "refs": [
                        {"title": "BBC Bitesize — Separating Mixtures", "url": "https://www.bbc.co.uk/bitesize/guides/zgvc4wx/revision/1"},
                        {"title": "Khan Academy — Mixtures and Solutions", "url": "https://www.khanacademy.org/science/chemistry/states-of-matter-and-intermolecular-forces"},
                        {"title": "Royal Society of Chemistry — Chromatography", "url": "https://edu.rsc.org/resources/chromatography/745.article"},
                    ],
                    "module": "simulators.chemistry.lower_secondary.separation_techniques",
                    "func": "simulate",
                },
                {
                    "name": "Chemical Reactions Explorer",
                    "icon": "🧪",
                    "desc": "What happens when substances react and form new materials",
                    "detail": (
                        "Classify reactions as combination, decomposition, or "
                        "displacement. Verify conservation of mass by comparing "
                        "reactant and product masses, and explore how temperature, "
                        "concentration, and surface area affect reaction speed."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Chemical Reactions", "url": "https://www.khanacademy.org/science/chemistry/chemical-reactions-stoichiome"},
                        {"title": "BBC Bitesize — Chemical Reactions", "url": "https://www.bbc.co.uk/bitesize/topics/zypsgk7"},
                        {"title": "PhET — Reactants, Products and Leftovers", "url": "https://phet.colorado.edu/en/simulations/reactants-products-and-leftovers"},
                    ],
                    "module": "simulators.chemistry.lower_secondary.chemical_reactions_intro",
                    "func": "simulate",
                },
            ],
            "📐 Mathematics": [
                {
                    "name": "Number Patterns & Sequences",
                    "icon": "🔢",
                    "desc": "Spot patterns in numbers and predict what comes next",
                    "detail": (
                        "Generate arithmetic sequences with a constant common "
                        "difference and geometric sequences with a constant ratio. "
                        "Visualise how each sequence grows and solve simple linear "
                        "equations interactively."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Sequences", "url": "https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:sequences"},
                        {"title": "Math is Fun — Sequences", "url": "https://www.mathsisfun.com/algebra/sequences-series.html"},
                        {"title": "BBC Bitesize — Sequences", "url": "https://www.bbc.co.uk/bitesize/topics/z2dqrwx"},
                    ],
                    "module": "simulators.maths.lower_secondary.number_and_algebra",
                    "func": "simulate",
                },
                {
                    "name": "Ratio & Proportion",
                    "icon": "⚖️",
                    "desc": "Divide quantities by ratio, scale shapes & work with percentages",
                    "detail": (
                        "Visualise ratio sharing with bar models — split a total "
                        "into two or three parts and see each share. Explore "
                        "direct proportion (y = kx) by scaling recipes or map "
                        "distances, and master percentages: find a percentage of "
                        "a number, calculate percentage change, and reverse "
                        "percentage problems."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Ratios and Proportions", "url": "https://www.khanacademy.org/math/cc-sixth-grade-math/cc-6th-ratios-and-rates"},
                        {"title": "BBC Bitesize — Ratio and Proportion", "url": "https://www.bbc.co.uk/bitesize/topics/zsq7hyc"},
                        {"title": "Math is Fun — Ratios", "url": "https://www.mathsisfun.com/numbers/ratio.html"},
                    ],
                    "module": "simulators.maths.lower_secondary.ratio_proportion",
                    "func": "simulate",
                },
                {
                    "name": "Geometry & Measurement",
                    "icon": "📏",
                    "desc": "Explore shapes, angles, area, and volume",
                    "detail": (
                        "Compute areas of rectangles, triangles, circles, and "
                        "parallelograms. Explore interior and exterior angles of "
                        "regular polygons and calculate the volume of cubes, "
                        "cuboids, cylinders, and spheres."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Geometry", "url": "https://www.khanacademy.org/math/geometry"},
                        {"title": "Math is Fun — Geometry", "url": "https://www.mathsisfun.com/geometry/index.html"},
                        {"title": "BBC Bitesize — Geometry", "url": "https://www.bbc.co.uk/bitesize/topics/zb6tyrd"},
                    ],
                    "module": "simulators.maths.lower_secondary.geometry_and_measures",
                    "func": "simulate",
                },
                {
                    "name": "Statistics & Probability",
                    "icon": "📊",
                    "desc": "Collect data, draw charts, and calculate probability",
                    "detail": (
                        "Calculate mean, median, mode, and range from custom data "
                        "sets. Run a probability simulator with adjustable trial "
                        "counts to see experimental vs theoretical probability, and "
                        "build bar charts, pie charts, and histograms."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Statistics and Probability", "url": "https://www.khanacademy.org/math/statistics-probability"},
                        {"title": "Math is Fun — Data", "url": "https://www.mathsisfun.com/data/index.html"},
                        {"title": "BBC Bitesize — Statistics", "url": "https://www.bbc.co.uk/bitesize/topics/z7rcwmn"},
                    ],
                    "module": "simulators.maths.lower_secondary.statistics_and_probability",
                    "func": "simulate",
                },
                {
                    "name": "Linear Equations & Graphs",
                    "icon": "📉",
                    "desc": "Solve equations, plot y = mx + c & shade inequalities",
                    "detail": (
                        "Solve linear equations of the form ax + b = c with an "
                        "interactive balance model. Graph straight lines y = mx + c "
                        "by adjusting gradient and intercept, and represent linear "
                        "inequalities on a number line with shaded regions."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Linear Equations", "url": "https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:solve-equations-inequalities"},
                        {"title": "BBC Bitesize — Linear Graphs", "url": "https://www.bbc.co.uk/bitesize/guides/zssqj6f/revision/1"},
                        {"title": "Math is Fun — Linear Equations", "url": "https://www.mathsisfun.com/algebra/linear-equations.html"},
                    ],
                    "module": "simulators.maths.lower_secondary.linear_equations",
                    "func": "simulate",
                },
            ],
        },
    },

    # ── Core STEM Pack ────────────────────────────────────────────────────────
    "📦 Core STEM (Grades 9–10)": {
        "icon": "🌍",
        "desc": "Exam-aligned simulators for IGCSE, ICSE, and CBSE — projectile motion, electricity, acids, reactions, graphs, and probability.",
        "subjects": {
            "🔬 Physics": [
                {
                    "name": "Kinematics — Motion Analysis",
                    "icon": "🏃",
                    "desc": "Displacement, velocity & acceleration with SUVAT equations",
                    "detail": (
                        "Study uniform and non-uniform motion using SUVAT equations "
                        "(s = ut + ½at², v = u + at, v² = u² + 2as). Plot "
                        "displacement-time, velocity-time, and acceleration-time "
                        "graphs and read off gradients and areas under curves."
                    ),
                    "refs": [
                        {"title": "Khan Academy — One-dimensional Motion", "url": "https://www.khanacademy.org/science/physics/one-dimensional-motion"},
                        {"title": "PhET — The Moving Man", "url": "https://phet.colorado.edu/en/simulations/the-moving-man"},
                        {"title": "HyperPhysics — Kinematics", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/mot.html"},
                    ],
                    "module": "simulators.physics.igcse_9_10.kinematics",
                    "func": "simulate",
                },
                {
                    "name": "Projectile Motion",
                    "icon": "🎯",
                    "desc": "Launch projectiles and trace parabolic trajectories",
                    "detail": (
                        "Launch a projectile at any angle and speed. Trace the "
                        "parabolic trajectory and analyse horizontal range, maximum "
                        "height, and flight time. Explore how launch angle affects "
                        "range — maximum at 45°."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Projectile Motion", "url": "https://www.khanacademy.org/science/physics/two-dimensional-motion"},
                        {"title": "PhET — Projectile Motion", "url": "https://phet.colorado.edu/en/simulations/projectile-motion"},
                        {"title": "HyperPhysics — Trajectories", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/traj.html"},
                    ],
                    "module": "simulators.physics.igcse_9_10.projectile_motion",
                    "func": "simulate",
                },
                {
                    "name": "Forces & Pressure",
                    "icon": "⚖️",
                    "desc": "Newton's laws and hydrostatic pressure",
                    "detail": (
                        "Apply Newton's Second Law (F = ma) to predict acceleration "
                        "and explore hydrostatic pressure (P = ρgh) in fluids. "
                        "Visualise how depth and fluid density affect pressure."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Forces and Newton's Laws", "url": "https://www.khanacademy.org/science/physics/forces-newtons-laws"},
                        {"title": "PhET — Forces and Motion", "url": "https://phet.colorado.edu/en/simulations/forces-and-motion-basics"},
                        {"title": "HyperPhysics — Pressure", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/press.html"},
                    ],
                    "module": "simulators.physics.igcse_9_10.forces_pressure",
                    "func": "simulate",
                },
                {
                    "name": "Electricity & Circuits",
                    "icon": "🔌",
                    "desc": "Ohm's law, series/parallel resistors & potential dividers",
                    "detail": (
                        "Plot V-I characteristics for ohmic resistors, filament "
                        "lamps, and diodes. Calculate equivalent resistance for "
                        "series and parallel networks of up to three resistors, "
                        "and design a potential divider to produce a target output "
                        "voltage using Vout = Vin × R₂/(R₁ + R₂)."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Circuits", "url": "https://www.khanacademy.org/science/physics/circuits-topic"},
                        {"title": "BBC Bitesize — Electricity", "url": "https://www.bbc.co.uk/bitesize/guides/zgr8d2p/revision/1"},
                        {"title": "PhET — Circuit Construction Kit: DC", "url": "https://phet.colorado.edu/en/simulations/circuit-construction-kit-dc"},
                    ],
                    "module": "simulators.physics.igcse_9_10.electricity",
                    "func": "simulate",
                },
                {
                    "name": "Waves & Light",
                    "icon": "🌈",
                    "desc": "Wave properties, Snell's law & total internal reflection",
                    "detail": (
                        "Explore transverse and longitudinal waves with adjustable "
                        "frequency and amplitude (v = fλ). Trace light rays through "
                        "boundaries using Snell's law (n₁ sin θ₁ = n₂ sin θ₂), and "
                        "discover the critical angle for total internal reflection "
                        "in optical fibres and prisms."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Light Waves", "url": "https://www.khanacademy.org/science/physics/geometric-optics"},
                        {"title": "PhET — Bending Light", "url": "https://phet.colorado.edu/en/simulations/bending-light"},
                        {"title": "HyperPhysics — Snell's Law", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/geoopt/refr.html"},
                    ],
                    "module": "simulators.physics.igcse_9_10.waves_light",
                    "func": "simulate",
                },
                {
                    "name": "Motion, Energy & Electricity — ICSE",
                    "icon": "⚡",
                    "desc": "Motion analysis, refraction, lenses & current electricity",
                    "detail": (
                        "Analyse distance-time and velocity-time graphs, calculate "
                        "kinetic and potential energy, study Snell's law and lens "
                        "behaviour, and explore Ohm's law with series and parallel "
                        "circuits."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Physics", "url": "https://www.khanacademy.org/science/physics"},
                        {"title": "Toppr — ICSE Physics", "url": "https://www.toppr.com/guides/physics/"},
                        {"title": "PhET — Circuit Construction Kit", "url": "https://phet.colorado.edu/en/simulations/circuit-construction-kit-dc"},
                    ],
                    "module": "simulators.physics.icse.icse_physics",
                    "func": "simulate",
                },
            ],
            "⚗️ Chemistry": [
                {
                    "name": "Atomic Structure Explorer",
                    "icon": "⚛️",
                    "desc": "Build atoms, study isotopes & electron configurations",
                    "detail": (
                        "Build atoms by choosing an element and see proton, neutron, "
                        "and electron counts. Explore isotopes, calculate relative "
                        "atomic mass, and write electron configurations using the "
                        "2.8.8 notation."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Atoms and the Periodic Table", "url": "https://www.khanacademy.org/science/chemistry/atomic-structure-and-properties"},
                        {"title": "PhET — Build an Atom", "url": "https://phet.colorado.edu/en/simulations/build-an-atom"},
                        {"title": "BBC Bitesize — Atomic Structure", "url": "https://www.bbc.co.uk/bitesize/guides/z8b2pv4/revision/1"},
                    ],
                    "module": "simulators.chemistry.igcse_9_10.atomic_structure",
                    "func": "simulate",
                },
                {
                    "name": "Chemical Bonding Lab",
                    "icon": "🔗",
                    "desc": "Compare ionic, covalent & metallic bonding",
                    "detail": (
                        "Explore how ionic bonds form through electron transfer, "
                        "covalent bonds through electron sharing, and metallic bonds "
                        "through a sea of delocalised electrons. Compare melting "
                        "points, conductivity, and structural properties."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Chemical Bonds", "url": "https://www.khanacademy.org/science/chemistry/chemical-bonds"},
                        {"title": "BBC Bitesize — Bonding", "url": "https://www.bbc.co.uk/bitesize/guides/z223qhv/revision/1"},
                        {"title": "PhET — Molecule Shapes", "url": "https://phet.colorado.edu/en/simulations/molecule-shapes"},
                    ],
                    "module": "simulators.chemistry.igcse_9_10.bonding",
                    "func": "simulate",
                },
                {
                    "name": "Reaction Types & Rates",
                    "icon": "⚡",
                    "desc": "Classify reactions and explore rate factors",
                    "detail": (
                        "Classify reactions as exothermic or endothermic, "
                        "combination, decomposition, or displacement. Investigate "
                        "how temperature, concentration, surface area, and catalysts "
                        "affect the rate of reaction."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Kinetics", "url": "https://www.khanacademy.org/science/chemistry/chem-kinetics"},
                        {"title": "BBC Bitesize — Rates of Reaction", "url": "https://www.bbc.co.uk/bitesize/guides/zsybjty/revision/1"},
                        {"title": "PhET — Reactions & Rates", "url": "https://phet.colorado.edu/en/simulations/reactions-and-rates"},
                    ],
                    "module": "simulators.chemistry.igcse_9_10.reactions",
                    "func": "simulate",
                },
                {
                    "name": "Acids, Bases & pH",
                    "icon": "🧪",
                    "desc": "The pH scale, neutralisation, and indicators",
                    "detail": (
                        "Explore the full pH scale from strong acids (0) to strong "
                        "bases (14). Mix acids and bases to observe neutralisation "
                        "and plot a titration curve. Test different indicators — "
                        "litmus, phenolphthalein, methyl orange, and universal "
                        "indicator — at any pH value."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Acids and Bases", "url": "https://www.khanacademy.org/science/chemistry/acids-and-bases-topic"},
                        {"title": "PhET — pH Scale", "url": "https://phet.colorado.edu/en/simulations/ph-scale"},
                        {"title": "BBC Bitesize — Acids and Bases", "url": "https://www.bbc.co.uk/bitesize/guides/z9bkwxs/revision/1"},
                    ],
                    "module": "simulators.chemistry.igcse_9_10.acids_bases",
                    "func": "simulate",
                },
                {
                    "name": "Acids, Bases & Organic Chemistry — ICSE",
                    "icon": "🧪",
                    "desc": "Acids / bases, periodic table trends & organic basics",
                    "detail": (
                        "Explore the pH scale with common acids and bases, study "
                        "periodic trends (atomic radius, ionisation energy, "
                        "electronegativity), and get an introduction to organic "
                        "chemistry with simple hydrocarbons."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Acids and Bases", "url": "https://www.khanacademy.org/science/chemistry/acids-and-bases-topic"},
                        {"title": "Toppr — ICSE Chemistry", "url": "https://www.toppr.com/guides/chemistry/"},
                        {"title": "PhET — pH Scale", "url": "https://phet.colorado.edu/en/simulations/ph-scale"},
                    ],
                    "module": "simulators.chemistry.icse.icse_chemistry",
                    "func": "simulate",
                },
            ],
            "📐 Mathematics": [
                {
                    "name": "Coordinate Geometry",
                    "icon": "📍",
                    "desc": "Points, distances, midpoints & line equations",
                    "detail": (
                        "Plot points on the Cartesian plane and calculate the "
                        "distance and midpoint between them. Find the equation of a "
                        "straight line (y = mx + c), determine gradients, and locate "
                        "line intersections."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Coordinate Geometry", "url": "https://www.khanacademy.org/math/geometry/hs-geo-analytic-geometry"},
                        {"title": "Math is Fun — Coordinate Geometry", "url": "https://www.mathsisfun.com/data/cartesian-coordinates.html"},
                        {"title": "BBC Bitesize — Straight Line Graphs", "url": "https://www.bbc.co.uk/bitesize/guides/zssqj6f/revision/1"},
                    ],
                    "module": "simulators.maths.igcse_9_10.coordinate_geometry",
                    "func": "simulate",
                },
                {
                    "name": "Functions & Graphs",
                    "icon": "📈",
                    "desc": "Linear, quadratic & cubic functions with transformations",
                    "detail": (
                        "Graph linear (y = mx + c), quadratic (y = ax² + bx + c), "
                        "and cubic functions. Apply vertical and horizontal "
                        "translations, reflections, and stretches to see how each "
                        "transformation changes the graph."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Functions", "url": "https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:functions"},
                        {"title": "Desmos Graphing Calculator", "url": "https://www.desmos.com/calculator"},
                        {"title": "Math is Fun — Function Grapher", "url": "https://www.mathsisfun.com/data/function-grapher.php"},
                    ],
                    "module": "simulators.maths.igcse_9_10.functions_graphs",
                    "func": "simulate",
                },
                {
                    "name": "Trigonometry",
                    "icon": "📐",
                    "desc": "Right-angle triangles, trig graphs, sine & cosine rules",
                    "detail": (
                        "Calculate sides and angles of right-angled triangles using "
                        "sin, cos, and tan. Plot sine, cosine, and tangent graphs "
                        "and apply the sine rule (a/sin A = b/sin B) and cosine "
                        "rule (a² = b² + c² − 2bc cos A) to any triangle."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Trigonometry", "url": "https://www.khanacademy.org/math/trigonometry"},
                        {"title": "Math is Fun — Trigonometry", "url": "https://www.mathsisfun.com/algebra/trigonometry.html"},
                        {"title": "BBC Bitesize — Trigonometry", "url": "https://www.bbc.co.uk/bitesize/guides/zsn2pv4/revision/1"},
                    ],
                    "module": "simulators.maths.igcse_9_10.trigonometry",
                    "func": "simulate",
                },
                {
                    "name": "Probability & Data Analysis",
                    "icon": "🎲",
                    "desc": "Dice simulation, probability trees & descriptive statistics",
                    "detail": (
                        "Roll dice and compare experimental vs theoretical "
                        "probability. Build two-stage probability trees for "
                        "independent events. Enter data sets to compute mean, "
                        "median, mode, range, and standard deviation with "
                        "histogram and box-plot visualisation."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Statistics and Probability", "url": "https://www.khanacademy.org/math/statistics-probability"},
                        {"title": "Math is Fun — Probability", "url": "https://www.mathsisfun.com/data/probability.html"},
                        {"title": "BBC Bitesize — Probability", "url": "https://www.bbc.co.uk/bitesize/guides/zp8wk2p/revision/1"},
                    ],
                    "module": "simulators.maths.igcse_9_10.probability_data",
                    "func": "simulate",
                },
                {
                    "name": "Quadratics, Circles & Statistics — ICSE",
                    "icon": "📊",
                    "desc": "Quadratic equations, circle geometry & statistics",
                    "detail": (
                        "Solve quadratic equations with the quadratic formula and "
                        "visualise their roots on a graph. Explore circle theorems, "
                        "tangent properties, and arc lengths, then compute "
                        "statistical measures like mean, median, and mode."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Quadratics", "url": "https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:quadratics-multiplying-factoring"},
                        {"title": "Toppr — ICSE Maths", "url": "https://www.toppr.com/guides/maths/"},
                        {"title": "Math is Fun — Circle", "url": "https://www.mathsisfun.com/geometry/circle.html"},
                    ],
                    "module": "simulators.maths.icse.icse_maths",
                    "func": "simulate",
                },
            ],
        },
    },

    # ── Advanced Pack ─────────────────────────────────────────────────────────
    "📦 Advanced (Grades 11–12)": {
        "icon": "🎓",
        "desc": "University-prep simulators for AS / A Level and CBSE — SHM, resonance, kinetics, vectors, thermodynamics, calculus, and statistics.",
        "subjects": {
            "🔬 Physics": [
                {
                    "name": "Kinematics & Dynamics — AS",
                    "icon": "🏎️",
                    "desc": "Advanced motion analysis and Newton's laws",
                    "detail": (
                        "Model uniformly accelerated motion with SUVAT equations in "
                        "one dimension. Apply Newton's three laws to calculate net "
                        "force, acceleration, and momentum in dynamic systems."
                    ),
                    "refs": [
                        {"title": "Cambridge AS Physics 9702 Syllabus", "url": "https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-international-as-and-a-level-physics-9702/"},
                        {"title": "Khan Academy — Forces and Motion", "url": "https://www.khanacademy.org/science/physics/forces-newtons-laws"},
                        {"title": "Isaac Physics — Dynamics", "url": "https://isaacphysics.org/topics/dynamics"},
                    ],
                    "module": "simulators.physics.cambridge_as.existing_simulators",
                    "func": "sim_kinematics_dynamics",
                },
                {
                    "name": "Projectile Motion — AS",
                    "icon": "🎯",
                    "desc": "2D projectile trajectories",
                    "detail": (
                        "Launch projectiles at any angle and speed and trace the "
                        "parabolic trajectory. Analyse horizontal range, maximum "
                        "height, and time of flight while resolving velocity into "
                        "horizontal and vertical components."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Projectile Motion", "url": "https://www.khanacademy.org/science/physics/two-dimensional-motion"},
                        {"title": "PhET — Projectile Motion", "url": "https://phet.colorado.edu/en/simulations/projectile-motion"},
                        {"title": "HyperPhysics — Trajectories", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/traj.html"},
                    ],
                    "module": "simulators.physics.cambridge_as.existing_simulators",
                    "func": "sim_projectile",
                },
                {
                    "name": "Forces, Density & Pressure — AS",
                    "icon": "🔧",
                    "desc": "Equilibrium, density & fluid pressure",
                    "detail": (
                        "Study coplanar forces in equilibrium, calculate density "
                        "from mass and volume, and compute hydrostatic pressure "
                        "(P = ρgh). Explore Archimedes' principle and buoyancy."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Fluids", "url": "https://www.khanacademy.org/science/physics/fluids"},
                        {"title": "HyperPhysics — Fluid Concepts", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/pflu.html"},
                        {"title": "Isaac Physics — Pressure", "url": "https://isaacphysics.org/topics/pressure"},
                    ],
                    "module": "simulators.physics.cambridge_as.existing_simulators",
                    "func": "sim_forces_density_pressure",
                },
                {
                    "name": "Waves & Superposition — AS",
                    "icon": "🌊",
                    "desc": "Wave properties, standing waves & interference",
                    "detail": (
                        "Visualise transverse and longitudinal waves with adjustable "
                        "wavelength, frequency, and amplitude. Generate standing "
                        "waves on a string, observe nodes and antinodes, and explore "
                        "constructive and destructive interference patterns."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Waves", "url": "https://www.khanacademy.org/science/physics/mechanical-waves-and-sound"},
                        {"title": "PhET — Wave on a String", "url": "https://phet.colorado.edu/en/simulations/wave-on-a-string"},
                        {"title": "HyperPhysics — Standing Waves", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/Waves/standw.html"},
                    ],
                    "module": "simulators.physics.cambridge_as.existing_simulators",
                    "func": "sim_waves_superposition",
                },
                {
                    "name": "D.C. Circuits — AS",
                    "icon": "🔌",
                    "desc": "Series / parallel circuits & Kirchhoff's laws",
                    "detail": (
                        "Build series and parallel circuits with resistors and "
                        "calculate total resistance, current, and voltage using "
                        "Ohm's law and Kirchhoff's current and voltage laws. "
                        "Explore power dissipation and internal resistance."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Circuits", "url": "https://www.khanacademy.org/science/physics/circuits-topic"},
                        {"title": "PhET — Circuit Construction Kit: DC", "url": "https://phet.colorado.edu/en/simulations/circuit-construction-kit-dc"},
                        {"title": "Isaac Physics — Electricity", "url": "https://isaacphysics.org/topics/electricity"},
                    ],
                    "module": "simulators.physics.cambridge_as.existing_simulators",
                    "func": "sim_dc_circuits",
                },
                {
                    "name": "Deformation of Solids — AS",
                    "icon": "📏",
                    "desc": "Stress-strain curves & material properties",
                    "detail": (
                        "Plot stress-strain curves for ductile and brittle "
                        "materials. Calculate Young's modulus from the linear "
                        "region, identify the yield point and ultimate tensile "
                        "strength, and compare elastic and plastic deformation."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Stress and Strain", "url": "https://www.khanacademy.org/science/physics/mechanical-waves-and-sound/stress-strain"},
                        {"title": "HyperPhysics — Elasticity", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/permot2.html"},
                        {"title": "Isaac Physics — Materials", "url": "https://isaacphysics.org/topics/materials"},
                    ],
                    "module": "simulators.physics.cambridge_as.existing_simulators",
                    "func": "sim_deformation_solids",
                },
                {
                    "name": "Simple Harmonic Motion — CBSE",
                    "icon": "🔄",
                    "desc": "Oscillations, springs & pendulums",
                    "detail": (
                        "Model the displacement x(t) = A sin(ωt + φ) for a mass on "
                        "a spring or a simple pendulum. Visualise velocity and "
                        "acceleration phases, and observe kinetic/potential energy "
                        "exchange with total energy conservation (E = ½kA²)."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Simple Harmonic Motion", "url": "https://www.khanacademy.org/science/physics/mechanical-waves-and-sound/harmonic-motion"},
                        {"title": "NCERT Physics Class 11 — Oscillations", "url": "https://ncert.nic.in/textbook.php?keph1=14-14"},
                        {"title": "PhET — Masses and Springs", "url": "https://phet.colorado.edu/en/simulations/masses-and-springs"},
                    ],
                    "module": "simulators.physics.cbse.simple_harmonic_motion",
                    "func": "simulate",
                },
                {
                    "name": "Wave Motion — CBSE",
                    "icon": "🌊",
                    "desc": "Transverse & longitudinal waves, Doppler effect",
                    "detail": (
                        "Generate transverse and longitudinal waves and observe "
                        "how wavelength, frequency, and amplitude relate via "
                        "v = fλ. Simulate the Doppler effect to see how relative "
                        "motion between source and observer shifts frequency."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Mechanical Waves", "url": "https://www.khanacademy.org/science/physics/mechanical-waves-and-sound"},
                        {"title": "NCERT Physics Class 11 — Waves", "url": "https://ncert.nic.in/textbook.php?keph1=15-15"},
                        {"title": "PhET — Wave Interference", "url": "https://phet.colorado.edu/en/simulations/wave-interference"},
                    ],
                    "module": "simulators.physics.cbse.waves",
                    "func": "simulate",
                },
                {
                    "name": "Thermal Physics & Oscillations — A Level",
                    "icon": "🌡️",
                    "desc": "Thermal energy, damped oscillations & circular motion",
                    "detail": (
                        "Model thermal energy transfer, specific heat capacity, and "
                        "latent heat. Simulate damped and forced oscillations with "
                        "resonance, and analyse uniform circular motion with "
                        "centripetal force and angular velocity."
                    ),
                    "refs": [
                        {"title": "Cambridge A Level Physics 9702 Syllabus", "url": "https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-international-as-and-a-level-physics-9702/"},
                        {"title": "HyperPhysics — Oscillations", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/shm.html"},
                        {"title": "Isaac Physics — Thermal Physics", "url": "https://isaacphysics.org/topics/thermal"},
                    ],
                    "module": "simulators.physics.cambridge_a.thermal_oscillations",
                    "func": "simulate",
                },
                {
                    "name": "Gravitational & Electric Fields — A Level",
                    "icon": "🌌",
                    "desc": "Radial fields, field strength, potential & orbits",
                    "detail": (
                        "Compute gravitational field strength g = GM/r² and "
                        "potential V = −GM/r around a massive body. Explore "
                        "electric field lines and Coulomb's law analogy, and "
                        "simulate circular orbits deriving orbital velocity, "
                        "period, and energy from first principles."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Gravitational Fields", "url": "https://www.khanacademy.org/science/physics/centripetal-force-and-gravitation"},
                        {"title": "Isaac Physics — Fields", "url": "https://isaacphysics.org/topics/fields"},
                        {"title": "HyperPhysics — Orbits", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/orbv.html"},
                    ],
                    "module": "simulators.physics.cambridge_a.fields",
                    "func": "simulate",
                },
                {
                    "name": "Electricity & Magnetism — CBSE",
                    "icon": "🧲",
                    "desc": "Coulomb's law, circuits & electromagnetic induction",
                    "detail": (
                        "Calculate electric fields using Coulomb's law and Gauss's "
                        "law. Solve DC circuits with Kirchhoff's laws, study "
                        "magnetic fields from current-carrying conductors, and "
                        "model electromagnetic induction with Faraday's law."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Electricity and Magnetism", "url": "https://www.khanacademy.org/science/physics/electric-charge-electric-force-and-voltage"},
                        {"title": "NCERT Physics Class 12 — Electrostatics", "url": "https://ncert.nic.in/textbook.php?leph1=1-1"},
                        {"title": "PhET — Faraday's Electromagnetic Lab", "url": "https://phet.colorado.edu/en/simulations/faradays-electromagnetic-lab"},
                    ],
                    "module": "simulators.physics.cbse.electricity_magnetism",
                    "func": "simulate",
                },
                {
                    "name": "Optics — CBSE",
                    "icon": "🔭",
                    "desc": "Ray diagrams, Young's double slit & single-slit diffraction",
                    "detail": (
                        "Draw ray diagrams for concave/convex mirrors and lenses "
                        "using the mirror/lens equation (1/f = 1/v − 1/u) and "
                        "compute magnification. Simulate Young's double-slit "
                        "experiment to observe constructive and destructive "
                        "interference fringes, and model single-slit Fraunhofer "
                        "diffraction with a sinc² intensity pattern."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Geometric Optics", "url": "https://www.khanacademy.org/science/physics/geometric-optics"},
                        {"title": "NCERT Physics Class 12 — Ray Optics", "url": "https://ncert.nic.in/textbook.php?leph1=9-9"},
                        {"title": "PhET — Geometric Optics", "url": "https://phet.colorado.edu/en/simulations/geometric-optics"},
                    ],
                    "module": "simulators.physics.cbse.optics",
                    "func": "simulate",
                },
                {
                    "name": "Resonance & Damped Oscillations",
                    "icon": "🔔",
                    "desc": "Damped oscillation regimes and driven resonance curves",
                    "detail": (
                        "Observe under-damped, critically-damped, and over-damped "
                        "motion with adjustable damping. Drive an oscillator at "
                        "varying frequencies to find the resonance peak and see how "
                        "damping broadens the response curve."
                    ),
                    "refs": [
                        {"title": "HyperPhysics — Damped Oscillations", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/oscda.html"},
                        {"title": "Khan Academy — Harmonic Motion", "url": "https://www.khanacademy.org/science/physics/mechanical-waves-and-sound/harmonic-motion"},
                        {"title": "Isaac Physics — Resonance", "url": "https://isaacphysics.org/topics/resonance"},
                    ],
                    "module": "simulators.physics.cambridge_a.resonance_damping",
                    "func": "simulate",
                },
            ],
            "⚗️ Chemistry": [
                {
                    "name": "Equilibrium Constant Kc — AS",
                    "icon": "⚖️",
                    "desc": "Calculate Kc and Le Chatelier's principle",
                    "detail": (
                        "Set initial concentrations for a reversible reaction and "
                        "compute the equilibrium constant Kc. Observe how changing "
                        "concentration, temperature, or pressure shifts the "
                        "equilibrium position as predicted by Le Chatelier's principle."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Equilibrium", "url": "https://www.khanacademy.org/science/chemistry/chemical-equilibrium"},
                        {"title": "Cambridge AS Chemistry 9701 Syllabus", "url": "https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-international-as-and-a-level-chemistry-9701/"},
                        {"title": "LibreTexts — Equilibrium Constants", "url": "https://chem.libretexts.org/Bookshelves/General_Chemistry/Map%3A_General_Chemistry_(Petrucci_et_al.)/15%3A_Principles_of_Chemical_Equilibrium"},
                    ],
                    "module": "simulators.chemistry.cambridge_as.equilibrium_kinetics",
                    "func": "simulate_equilibrium",
                },
                {
                    "name": "Rate of Reaction — AS",
                    "icon": "⏱️",
                    "desc": "Arrhenius equation & activation energy",
                    "detail": (
                        "Use the Arrhenius equation (k = A·e^(-Ea/RT)) to model how "
                        "temperature and activation energy affect reaction rate. "
                        "Plot Arrhenius curves and energy profile diagrams showing "
                        "reactants, products, and the activation energy barrier."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Kinetics", "url": "https://www.khanacademy.org/science/chemistry/chem-kinetics"},
                        {"title": "PhET — Reactions & Rates", "url": "https://phet.colorado.edu/en/simulations/reactions-and-rates"},
                        {"title": "LibreTexts — Arrhenius Equation", "url": "https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_Theoretical_Chemistry)/Kinetics/06%3A_Modeling_Reaction_Kinetics/6.02%3A_Temperature_Dependence_of_Reaction_Rates/6.2.03%3A_The_Arrhenius_Law/6.2.3.01%3A_Arrhenius_Equation"},
                    ],
                    "module": "simulators.chemistry.cambridge_as.equilibrium_kinetics",
                    "func": "simulate_rate_reaction",
                },
                {
                    "name": "Thermochemistry — AS",
                    "icon": "🔥",
                    "desc": "Enthalpy changes & Hess's law",
                    "detail": (
                        "Calculate standard enthalpy changes (ΔH) for exothermic "
                        "and endothermic reactions using Hess's law and bond "
                        "energies. Visualise energy bar charts and enthalpy level "
                        "diagrams."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Thermochemistry", "url": "https://www.khanacademy.org/science/chemistry/thermodynamics-chemistry"},
                        {"title": "LibreTexts — Enthalpy", "url": "https://chem.libretexts.org/Bookshelves/General_Chemistry/Map%3A_General_Chemistry_(Petrucci_et_al.)/07%3A_Thermochemistry"},
                        {"title": "BBC Bitesize — Energy Changes", "url": "https://www.bbc.co.uk/bitesize/guides/z2g2pv4/revision/1"},
                    ],
                    "module": "simulators.chemistry.cambridge_as.equilibrium_kinetics",
                    "func": "simulate_thermochemistry",
                },
                {
                    "name": "Ideal Gas Law (PV = nRT) — AS",
                    "icon": "💨",
                    "desc": "Gas behaviour & the combined gas law",
                    "detail": (
                        "Explore PV = nRT by adjusting pressure, volume, "
                        "temperature, and number of moles. Apply the combined gas "
                        "law (P₁V₁/T₁ = P₂V₂/T₂) to predict state changes and "
                        "visualise the relationships on interactive graphs."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Gases", "url": "https://www.khanacademy.org/science/chemistry/gases-and-kinetic-molecular-theory"},
                        {"title": "PhET — Gas Properties", "url": "https://phet.colorado.edu/en/simulations/gas-properties"},
                        {"title": "HyperPhysics — Ideal Gas Law", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/Kinetic/idegas.html"},
                    ],
                    "module": "simulators.chemistry.cambridge_as.gas_laws",
                    "func": "simulate",
                },
                {
                    "name": "Equilibrium, Acids & Thermodynamics — CBSE",
                    "icon": "🧪",
                    "desc": "Chemical equilibrium, pH & enthalpy",
                    "detail": (
                        "Study chemical equilibrium and Le Chatelier's principle, "
                        "explore the pH scale with buffer solutions and "
                        "neutralisation, and calculate enthalpy changes for "
                        "common reactions."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Chemical Equilibrium", "url": "https://www.khanacademy.org/science/chemistry/chemical-equilibrium"},
                        {"title": "NCERT Chemistry Class 11 — Equilibrium", "url": "https://ncert.nic.in/textbook.php?kech1=7-7"},
                        {"title": "PhET — Acid-Base Solutions", "url": "https://phet.colorado.edu/en/simulations/acid-base-solutions"},
                    ],
                    "module": "simulators.chemistry.cbse.cbse_chemistry",
                    "func": "simulate",
                },
                {
                    "name": "Atomic Structure & Periodic Table — CBSE",
                    "icon": "⚛️",
                    "desc": "Quantum numbers, electron configuration & periodic trends",
                    "detail": (
                        "Explore the four quantum numbers (n, l, ml, ms) and "
                        "visualise radial probability distributions for s, p, and "
                        "d orbitals. Build electron configurations using the "
                        "Aufbau principle and Hund's rule, and plot periodic "
                        "trends — atomic radius, ionisation energy, and "
                        "electronegativity — for elements Z = 1 to 20."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Electronic Structure of Atoms", "url": "https://www.khanacademy.org/science/chemistry/electronic-structure-of-atoms"},
                        {"title": "NCERT Chemistry Class 11 — Structure of Atom", "url": "https://ncert.nic.in/textbook.php?kech1=2-2"},
                        {"title": "PhET — Build an Atom", "url": "https://phet.colorado.edu/en/simulations/build-an-atom"},
                    ],
                    "module": "simulators.chemistry.cbse.atomic_structure_periodic",
                    "func": "simulate",
                },
                {
                    "name": "Advanced Chemistry — A Level",
                    "icon": "🧬",
                    "desc": "Kinetics, equilibrium Kp & electrochemistry",
                    "detail": (
                        "Explore reaction orders and rate laws, compute the "
                        "equilibrium constant Kp for gaseous reactions, and model "
                        "electrochemical cells with standard electrode potentials "
                        "and the Nernst equation."
                    ),
                    "refs": [
                        {"title": "Cambridge A Level Chemistry 9701 Syllabus", "url": "https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-international-as-and-a-level-chemistry-9701/"},
                        {"title": "Khan Academy — Electrochemistry", "url": "https://www.khanacademy.org/science/chemistry/oxidation-reduction"},
                        {"title": "LibreTexts — Equilibrium", "url": "https://chem.libretexts.org/Bookshelves/General_Chemistry/Map%3A_General_Chemistry_(Petrucci_et_al.)/15%3A_Principles_of_Chemical_Equilibrium"},
                    ],
                    "module": "simulators.chemistry.cambridge_a.advanced_chemistry",
                    "func": "simulate",
                },
                {
                    "name": "Organic Chemistry — A Level",
                    "icon": "⬡",
                    "desc": "Homologous series, functional groups & reaction pathways",
                    "detail": (
                        "Compare boiling-point and melting-point trends for "
                        "alkanes, alkenes, and alcohols by chain length. Explore "
                        "structural isomerism and track how isomer count grows "
                        "with carbon number. Map multi-step reaction pathways "
                        "between functional groups and find the shortest synthetic "
                        "route using a network graph."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Organic Chemistry", "url": "https://www.khanacademy.org/science/organic-chemistry"},
                        {"title": "Cambridge A Level Chemistry 9701", "url": "https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-international-as-and-a-level-chemistry-9701/"},
                        {"title": "LibreTexts — Organic Reactions", "url": "https://chem.libretexts.org/Bookshelves/Organic_Chemistry"},
                    ],
                    "module": "simulators.chemistry.cambridge_a.organic_chemistry",
                    "func": "simulate",
                },
                {
                    "name": "Chemical Kinetics Laboratory",
                    "icon": "⏱️",
                    "desc": "Reaction orders, Arrhenius plots & half-life analysis",
                    "detail": (
                        "Compare zero, first, and second order kinetics with "
                        "diagnostic plots (ln[A] vs t, 1/[A] vs t). Plot an "
                        "Arrhenius graph to determine activation energy, and "
                        "calculate half-lives for each reaction order."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Kinetics", "url": "https://www.khanacademy.org/science/chemistry/chem-kinetics"},
                        {"title": "LibreTexts — Reaction Kinetics", "url": "https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_Theoretical_Chemistry)/Kinetics"},
                        {"title": "Isaac Chemistry — Rates", "url": "https://isaacphysics.org/topics/reaction_rates"},
                    ],
                    "module": "simulators.chemistry.cambridge_a.kinetics_lab",
                    "func": "simulate",
                },
            ],
            "📐 Mathematics": [
                {
                    "name": "Algebra & Functions — AS",
                    "icon": "🔤",
                    "desc": "Quadratics, inequalities, functions & partial fractions",
                    "detail": (
                        "Solve and graph quadratic equations and inequalities. "
                        "Explore domain, range, composite functions, and inverse "
                        "functions. Decompose rational expressions into partial "
                        "fractions and transform function graphs."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Algebra", "url": "https://www.khanacademy.org/math/algebra2"},
                        {"title": "Cambridge AS Maths 9709 Syllabus", "url": "https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-international-as-and-a-level-mathematics-9709/"},
                        {"title": "Math is Fun — Algebra", "url": "https://www.mathsisfun.com/algebra/index.html"},
                    ],
                    "module": "simulators.maths.cambridge_as.algebra_functions",
                    "func": "simulate",
                },
                {
                    "name": "Calculus — AS",
                    "icon": "∫",
                    "desc": "Differentiation, integration & stationary points",
                    "detail": (
                        "Differentiate polynomial, trigonometric, and exponential "
                        "functions. Find stationary points and determine their "
                        "nature (maxima, minima, inflection). Integrate functions "
                        "and calculate areas under curves."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Calculus 1", "url": "https://www.khanacademy.org/math/calculus-1"},
                        {"title": "3Blue1Brown — Essence of Calculus", "url": "https://www.3blue1brown.com/topics/calculus"},
                        {"title": "Math is Fun — Calculus", "url": "https://www.mathsisfun.com/calculus/index.html"},
                    ],
                    "module": "simulators.maths.cambridge_as.calculus",
                    "func": "simulate",
                },
                {
                    "name": "Limits, Derivatives & Calculus — CBSE",
                    "icon": "📊",
                    "desc": "Limits, differentiation, integration & vectors",
                    "detail": (
                        "Visualise limits graphically and numerically, differentiate "
                        "polynomial and trigonometric functions, and integrate to "
                        "find areas. Explore 2D and 3D vectors with dot and cross "
                        "products."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Calculus", "url": "https://www.khanacademy.org/math/calculus-1"},
                        {"title": "NCERT Maths Class 11 — Limits and Derivatives", "url": "https://ncert.nic.in/textbook.php?kemh1=13-13"},
                        {"title": "Math is Fun — Calculus", "url": "https://www.mathsisfun.com/calculus/index.html"},
                    ],
                    "module": "simulators.maths.cbse.cbse_maths",
                    "func": "simulate",
                },
                {
                    "name": "Advanced Mathematics — A Level",
                    "icon": "∞",
                    "desc": "Integration techniques, differential equations & vectors",
                    "detail": (
                        "Apply advanced integration techniques (substitution, parts, "
                        "partial fractions), solve first-order differential "
                        "equations, and work with 3D vectors including cross "
                        "products and lines/planes in space."
                    ),
                    "refs": [
                        {"title": "Cambridge A Level Maths 9709 Syllabus", "url": "https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-international-as-and-a-level-mathematics-9709/"},
                        {"title": "Khan Academy — Calculus 2", "url": "https://www.khanacademy.org/math/calculus-2"},
                        {"title": "3Blue1Brown — Essence of Linear Algebra", "url": "https://www.3blue1brown.com/topics/linear-algebra"},
                    ],
                    "module": "simulators.maths.cambridge_a.advanced_maths",
                    "func": "simulate",
                },
                {
                    "name": "Statistics & Probability — A Level",
                    "icon": "📊",
                    "desc": "Normal & binomial distributions and hypothesis testing",
                    "detail": (
                        "Explore the Normal distribution N(μ, σ²) with adjustable "
                        "mean and standard deviation — shade areas and compute "
                        "probabilities using Z-scores. Generate binomial "
                        "distributions B(n, p) and overlay the normal "
                        "approximation. Perform a one-sample Z-test of a "
                        "population mean at a chosen significance level and "
                        "visualise the rejection region."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Statistics & Probability", "url": "https://www.khanacademy.org/math/statistics-probability"},
                        {"title": "Cambridge A Level Maths 9709 — Probability & Statistics", "url": "https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-international-as-and-a-level-mathematics-9709/"},
                        {"title": "Stat Trek — Normal Distribution", "url": "https://stattrek.com/probability-distributions/normal"},
                    ],
                    "module": "simulators.maths.cambridge_a.statistics_probability",
                    "func": "simulate",
                },
                {
                    "name": "Vectors & 3D Geometry",
                    "icon": "📐",
                    "desc": "Vector operations, dot/cross products, lines & planes",
                    "detail": (
                        "Add, subtract, and scale 3D vectors with real-time "
                        "visualisation. Compute dot and cross products, find "
                        "angles between vectors, and calculate the distance "
                        "from a point to a plane."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Linear Algebra", "url": "https://www.khanacademy.org/math/linear-algebra"},
                        {"title": "3Blue1Brown — Essence of Linear Algebra", "url": "https://www.3blue1brown.com/topics/linear-algebra"},
                        {"title": "Math is Fun — Vectors", "url": "https://www.mathsisfun.com/algebra/vectors.html"},
                    ],
                    "module": "simulators.maths.cambridge_a.vectors_3d",
                    "func": "simulate",
                },
            ],
        },
    },

    # ── Cross-Disciplinary Enrichment Pack ────────────────────────────────────
    "🌐 Cross-Disciplinary Enrichment": {
        "icon": "🧩",
        "desc": "Real-world STEM projects that blend physics, maths, biology, and computing.",
        "subjects": {
            "🌐 Applied STEM": [
                {
                    "name": "Bridge Design Challenge",
                    "icon": "🌉",
                    "desc": "Design a beam bridge and analyse stress, deflection & bending moments",
                    "detail": (
                        "Choose a material (steel, aluminium, wood, concrete), set "
                        "beam dimensions and loading, and observe the deflection "
                        "curve and bending moment diagram. Test a Warren truss "
                        "under load and calculate reaction forces."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Mechanics of Materials", "url": "https://www.khanacademy.org/science/physics"},
                        {"title": "Engineering Toolbox — Beam Deflection", "url": "https://www.engineeringtoolbox.com/beam-stress-deflection-d_1312.html"},
                        {"title": "PBS — Building Big: Bridges", "url": "https://www.pbs.org/wgbh/buildingbig/bridge/index.html"},
                    ],
                    "module": "simulators.cross_disciplinary.bridge_design",
                    "func": "simulate",
                },
                {
                    "name": "Climate Modelling",
                    "icon": "🌍",
                    "desc": "Energy-balance model and greenhouse effect layers",
                    "detail": (
                        "Use a zero-dimensional energy-balance model to find "
                        "Earth's equilibrium temperature. Adjust solar constant, "
                        "albedo, and emissivity, then add atmospheric layers to "
                        "model the greenhouse effect and see how surface "
                        "temperature rises."
                    ),
                    "refs": [
                        {"title": "NASA — Climate Science", "url": "https://climate.nasa.gov/"},
                        {"title": "Khan Academy — Earth Science", "url": "https://www.khanacademy.org/science/earth-science"},
                        {"title": "PhET — The Greenhouse Effect", "url": "https://phet.colorado.edu/en/simulations/greenhouse-effect"},
                    ],
                    "module": "simulators.cross_disciplinary.climate_model",
                    "func": "simulate",
                },
                {
                    "name": "Epidemiology — SIR Model",
                    "icon": "🦠",
                    "desc": "Simulate disease spread with the SIR compartmental model",
                    "detail": (
                        "Divide a population into Susceptible, Infected, and Recovered "
                        "compartments. Adjust transmission rate β and recovery rate γ "
                        "to observe epidemic curves, compute R₀, and explore herd "
                        "immunity through vaccination coverage."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Epidemiology", "url": "https://www.khanacademy.org/science/health-and-medicine/infectious-diseases"},
                        {"title": "3Blue1Brown — Simulating an Epidemic", "url": "https://www.youtube.com/watch?v=gxAaO2rsdIs"},
                        {"title": "Wikipedia — SIR Model", "url": "https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology"},
                    ],
                    "module": "simulators.cross_disciplinary.epidemiology",
                    "func": "simulate",
                },
                {
                    "name": "Coding & Mathematics",
                    "icon": "💻",
                    "desc": "Sorting algorithms, Fibonacci sequence & fractal patterns",
                    "detail": (
                        "Step through bubble, selection, and insertion sorts to "
                        "compare algorithmic complexity. Explore the Fibonacci "
                        "sequence and its convergence to the golden ratio, then "
                        "generate fractals — the Mandelbrot set and Sierpinski "
                        "triangle — using iterative mathematics."
                    ),
                    "refs": [
                        {"title": "Khan Academy — Algorithms", "url": "https://www.khanacademy.org/computing/computer-science/algorithms"},
                        {"title": "3Blue1Brown — Fractals", "url": "https://www.3blue1brown.com/topics/fractals"},
                        {"title": "Visualgo — Sorting", "url": "https://visualgo.net/en/sorting"},
                    ],
                    "module": "simulators.cross_disciplinary.coding_maths",
                    "func": "simulate",
                },
            ],
        },
    },
}


def get_stats():
    """Return aggregate statistics for the home page."""
    total = 0
    subjects = set()
    for pack in CATALOG.values():
        for subj, topics in pack["subjects"].items():
            subjects.add(subj)
            total += len(topics)
    return {"packs": len(CATALOG), "subjects": len(subjects), "simulators": total}
