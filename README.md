# stem-simulators-lab
# 🔬 STEM Lab — Interactive Science & Mathematics Simulators

**Open-source educational platform · 4 themed simulator packs · Apache License 2.0**

[![Streamlit](https://img.shields.io/badge/Built_with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![License: Apache License 2.0](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://python.org)

---

## ✨ Features

- **62 interactive simulators** spanning Physics, Chemistry, Mathematics, and Applied STEM
- **4 themed packs**: Foundation (Grades 6–8), Core STEM (Grades 9–10), Advanced (Grades 11–12), Cross-Disciplinary Enrichment
- **Pack-based navigation** — choose a pack, subject, then topic
- **Authentication**: Secure signup/login with bcrypt password hashing
- **Audit Trail**: Full activity logging for every user action
- **Admin Dashboard**: User management, role assignment, audit log viewer
- **User Profiles**: Password management, personal activity history
- **Session Management**: Automatic timeout, account lockout on failed attempts
- **Guardrails**: Input sanitization, rate limiting, password strength policy, concurrent session limiting, error boundaries
- **Legal Compliance**: Terms of Service and Privacy Policy pages
- **Structured Logging**: Rotating file logs for application and audit events
- **Enterprise UI** with hero banner, topic cards, breadcrumbs, and professional styling
- **Dynamic loading** — simulators load on demand for fast startup
- **Real-time visualisations** powered by Matplotlib and NumPy

---

## � Simulator Packs

| Pack | Age Range | Subjects | Simulators |
|------|-----------|----------|------------|
| 🔰 Foundation (Grades 6–8) | 11–14 | Physics, Chemistry, Mathematics | 14 |
| 🌍 Core STEM (Grades 9–10) | 14–16 | Physics, Chemistry, Mathematics | 16 |
| 🎓 Advanced (Grades 11–12) | 16–18 | Physics, Chemistry, Mathematics | 28 |
| 🧩 Cross-Disciplinary Enrichment | All ages | Applied STEM | 4 |

---

## 🧪 Full Simulator Catalog

Every simulator includes a detailed description and curated reference links to Khan Academy, PhET, BBC Bitesize, and other trusted educational resources.

### 📦 Foundation (Grades 6–8)

| Subject | Simulator | Description |
|---------|-----------|-------------|
| 🔬 Physics | **Forces & Motion Basics** | Explore speed = distance ÷ time, Newton's Second Law (F = ma), and friction on different surfaces |
| 🔬 Physics | **Simple Circuits** | Build battery-and-bulb circuits, compare conductors vs insulators, explore series & parallel |
| 🔬 Physics | **Energy Transfers & Forces** | Kinetic/potential energy conversions, ball drop conservation, Newton's law of cooling |
| 🔬 Physics | **Magnets & Magnetic Fields** | Magnetic field lines (streamplot dipole), compass needle, electromagnet strength (B = μ₀NI/L) |
| 🔬 Physics | **Light & Sound Waves** | Law of reflection, Snell's law refraction, transverse sound waves with adjustable frequency |
| ⚗️ Chemistry | **States of Matter** | Particle model for solids, liquids, gases; heating curves from ice to steam; density comparison |
| ⚗️ Chemistry | **Elements & Compounds** | Periodic table (first 20 elements), elements vs compounds, balancing word equations |
| ⚗️ Chemistry | **Separation Techniques** | Filtration, evaporation & distillation (heating curves), chromatography (Rf values) |
| ⚗️ Chemistry | **Chemical Reactions Explorer** | Classify reaction types, conservation of mass, temperature/concentration/surface area effects |
| 📐 Maths | **Number Patterns & Sequences** | Arithmetic and geometric sequences, visualise growth, solve simple linear equations |
| 📐 Maths | **Ratio & Proportion** | Bar-model ratios (2- and 3-part), direct proportion scaling, percentage calculator |
| 📐 Maths | **Geometry & Measurement** | Areas of shapes, polygon angles, volume of cubes, cuboids, cylinders, spheres |
| 📐 Maths | **Statistics & Probability** | Mean/median/mode/range, experimental vs theoretical probability, bar/pie/histogram charts |
| 📐 Maths | **Linear Equations & Graphs** | Solve ax + b = c with balance model, graph y = mx + c, shade inequalities on number line |

### 📦 Core STEM (Grades 9–10)

| Subject | Simulator | Description |
|---------|-----------|-------------|
| 🔬 Physics | **Kinematics — Motion Analysis** | SUVAT equations, displacement-time, velocity-time, and acceleration-time graphs |
| 🔬 Physics | **Projectile Motion** | Launch projectiles at any angle, trace parabolic trajectories, analyse range vs launch angle |
| 🔬 Physics | **Forces & Pressure** | Newton's Second Law (F = ma), hydrostatic pressure (P = ρgh), fluid depth effects |
| 🔬 Physics | **Electricity & Circuits** | Ohm's law V-I graphs (ohmic/filament/diode), series/parallel resistors, potential dividers |
| 🔬 Physics | **Waves & Light** | Wave properties (v = fλ), Snell's law ray diagrams, total internal reflection & critical angle |
| 🔬 Physics | **Motion, Energy & Electricity — ICSE** | Distance-time/velocity-time graphs, KE/PE, Snell's law, Ohm's law circuits |
| ⚗️ Chemistry | **Atomic Structure Explorer** | Build atoms, explore isotopes, calculate relative atomic mass, electron configurations |
| ⚗️ Chemistry | **Chemical Bonding Lab** | Ionic, covalent, and metallic bonding; melting points, conductivity, structural properties |
| ⚗️ Chemistry | **Reaction Types & Rates** | Exo/endothermic classification, temperature/concentration/catalyst effects on rate |
| ⚗️ Chemistry | **Acids, Bases & pH** | pH scale, neutralisation titration curves, acid-base indicators at any pH value |
| ⚗️ Chemistry | **Acids, Bases & Organic Chemistry — ICSE** | pH scale, periodic trends, introduction to hydrocarbons |
| 📐 Maths | **Coordinate Geometry** | Cartesian plotting, distance/midpoint, line equations (y = mx + c), intersections |
| 📐 Maths | **Functions & Graphs** | Linear, quadratic, cubic functions; translations, reflections, stretches |
| 📐 Maths | **Trigonometry** | Right-angle trig (sin/cos/tan), trig graphs, sine rule, cosine rule |
| 📐 Maths | **Probability & Data Analysis** | Dice simulation, probability trees, mean/median/mode/range with histograms & box plots |
| 📐 Maths | **Quadratics, Circles & Statistics — ICSE** | Quadratic formula, circle theorems, mean/median/mode |

### 📦 Advanced (Grades 11–12)

| Subject | Simulator | Description |
|---------|-----------|-------------|
| 🔬 Physics | **Kinematics & Dynamics — AS** | SUVAT in 1D, Newton's three laws, net force and momentum |
| 🔬 Physics | **Projectile Motion — AS** | Parabolic trajectories, range, max height, time of flight |
| 🔬 Physics | **Forces, Density & Pressure — AS** | Coplanar equilibrium, density, hydrostatic pressure, Archimedes' principle |
| 🔬 Physics | **Waves & Superposition — AS** | Transverse/longitudinal waves, standing waves, interference patterns |
| 🔬 Physics | **D.C. Circuits — AS** | Series/parallel resistors, Ohm's law, Kirchhoff's laws, internal resistance |
| 🔬 Physics | **Deformation of Solids — AS** | Stress-strain curves, Young's modulus, yield point, elastic vs plastic deformation |
| 🔬 Physics | **Simple Harmonic Motion — CBSE** | x(t) = A sin(ωt + φ), springs, pendulums, KE/PE exchange |
| 🔬 Physics | **Wave Motion — CBSE** | Transverse/longitudinal waves, v = fλ, Doppler effect |
| 🔬 Physics | **Thermal Physics & Oscillations — A Level** | Specific heat, latent heat, damped/forced oscillations, circular motion |
| 🔬 Physics | **Gravitational & Electric Fields — A Level** | g = GM/r², electric field lines, orbital mechanics (velocity, period) |
| 🔬 Physics | **Electricity & Magnetism — CBSE** | Coulomb's/Gauss's law, Kirchhoff circuits, Faraday's law of induction |
| 🔬 Physics | **Optics — CBSE** | Ray diagrams (1/f = 1/v − 1/u), Young's double slit, single-slit diffraction |
| 🔬 Physics | **Resonance & Damped Oscillations** | Damped oscillation regimes, driven resonance curves, Q-factor analysis |
| ⚗️ Chemistry | **Equilibrium Constant Kc — AS** | Calculate Kc, Le Chatelier's principle, concentration/temperature/pressure shifts |
| ⚗️ Chemistry | **Rate of Reaction — AS** | Arrhenius equation (k = A·e^(-Ea/RT)), energy profiles, activation energy |
| ⚗️ Chemistry | **Thermochemistry — AS** | Enthalpy changes (ΔH), Hess's law, bond energies, energy bar charts |
| ⚗️ Chemistry | **Ideal Gas Law (PV = nRT) — AS** | Combined gas law, state changes, interactive P-V-T graphs |
| ⚗️ Chemistry | **Equilibrium, Acids & Thermodynamics — CBSE** | Le Chatelier's principle, pH/buffers, enthalpy calculations |
| ⚗️ Chemistry | **Atomic Structure & Periodic Table — CBSE** | Quantum numbers, electron configuration (Aufbau), periodic trends for Z = 1–20 |
| ⚗️ Chemistry | **Advanced Chemistry — A Level** | Reaction orders, rate laws, Kp, electrochemical cells, Nernst equation |
| ⚗️ Chemistry | **Organic Chemistry — A Level** | Homologous series BP/MP trends, structural isomerism, reaction pathway network graph |
| ⚗️ Chemistry | **Chemical Kinetics Laboratory** | Reaction orders, Arrhenius plots, half-life analysis for zero/first/second order |
| 📐 Maths | **Algebra & Functions — AS** | Quadratics, inequalities, composite/inverse functions, partial fractions |
| 📐 Maths | **Calculus — AS** | Differentiation, integration, stationary points, areas under curves |
| 📐 Maths | **Limits, Derivatives & Calculus — CBSE** | Graphical limits, differentiation, integration, 2D/3D vectors |
| 📐 Maths | **Advanced Mathematics — A Level** | Integration techniques, differential equations, 3D vectors, lines/planes |
| 📐 Maths | **Statistics & Probability — A Level** | Normal/binomial distributions, Z-scores, hypothesis testing (one-sample Z-test) |
| 📐 Maths | **Vectors & 3D Geometry** | Vector operations, dot/cross products, point-to-plane distance, 3D visualisation |

### 🌐 Cross-Disciplinary Enrichment

| Subject | Simulator | Description |
|---------|-----------|-------------|
| 🌐 Applied STEM | **Bridge Design Challenge** | Beam bridge stress & deflection, bending moment diagrams, Warren truss analysis |
| 🌐 Applied STEM | **Climate Modelling** | Zero-dimensional energy-balance model, greenhouse effect layers, equilibrium temperature |
| 🌐 Applied STEM | **Epidemiology — SIR Model** | Susceptible-Infected-Recovered dynamics, R₀ computation, herd immunity via vaccination |
| 🌐 Applied STEM | **Coding & Mathematics** | Sorting algorithm visualiser, Fibonacci & golden ratio, Mandelbrot & Sierpinski fractals |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or later

### Install & Run

```bash
git clone https://github.com/your-username/stem-simulators.git
cd stem-simulators
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Copy and configure environment (optional — defaults work out of the box)
cp .env.example .env
# Edit .env to set STEMLAB_SECRET_KEY for production

streamlit run app.py
```

The app opens at `http://localhost:8501`.

### Testing

The project includes comprehensive unit tests for core functionality.

```bash
# Install test dependencies (pytest is already in requirements.txt)
pip install -r requirements.txt

# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run tests with coverage
pytest --cov=core --cov=simulators
```

### First-Time Setup

1. Open the app and click **Sign Up** to create an account.
2. The first user can be promoted to admin via the SQLite database:
   ```bash
   sqlite3 data/stemlab.db "UPDATE users SET role='admin' WHERE username='your_username';"
   ```
3. Admin users see the **🛡️ Admin** page for user management and audit logs.

### Deploy to Streamlit Cloud

1. Push to GitHub (the `data/` and `logs/` directories are git-ignored)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Set secrets: `STEMLAB_SECRET_KEY` in the Streamlit Cloud secrets panel
4. Connect the repo → set **app.py** as entry point → Deploy

---

## 🗂️ Project Structure

```
stem-simulators/
├── app.py                     # Main application (auth, routing, admin)
├── requirements.txt           # Dependencies
├── .env.example               # Environment variable template
├── .streamlit/config.toml     # Theme configuration
├── LICENSE                    # Apache License 2.0
├── core/                      # Platform infrastructure (auth, logging, audit, guardrails)
│   ├── settings.py            # Centralised env-based configuration
│   ├── database.py            # SQLite database layer (users, sessions, audit)
│   ├── auth.py                # Authentication (signup, login, sessions, bcrypt)
│   ├── guardrails.py          # Input sanitization, rate limiting, password policy
│   ├── logger.py              # Rotating file + console logging
│   ├── audit.py               # Audit trail (DB + file)
│   └── admin.py               # Admin dashboard helpers
├── data/                      # SQLite database (auto-created, git-ignored)
├── logs/                      # Application & audit logs (auto-created, git-ignored)
├── docs/
│   ├── USER_GUIDE.md          # End-user guide
│   └── TECHNICAL_DOCS.md      # Developer documentation
└── simulators/
    ├── config.py              # Simulator catalog / registry (pack-based)
    ├── utils.py               # Shared helpers
    ├── physics/
    │   ├── lower_secondary/   # Foundation pack sims
    │   ├── igcse_9_10/        # Core STEM pack sims
    │   ├── cambridge_as/      # Advanced pack — AS Level
    │   ├── cambridge_a/       # Advanced pack — A Level
    │   ├── cbse/              # Advanced pack — CBSE
    │   └── icse/              # Core STEM pack — ICSE
    ├── chemistry/             # (same sub-folders)
    ├── maths/                 # (same sub-folders)
    └── cross_disciplinary/    # Cross-Disciplinary Enrichment pack
```

---

## 🛠️ Adding a New Simulator

1. Create `simulators/<subject>/<level>/<topic>.py` with a `simulate()` function.
2. Register it in `simulators/config.py` under the appropriate pack → subject.
3. Run the app and navigate to the new topic.

See [Technical Docs](docs/TECHNICAL_DOCS.md) for the full module contract.

---

## 📖 Documentation

- [User Guide](docs/USER_GUIDE.md) — how to use the platform
- [Technical Docs](docs/TECHNICAL_DOCS.md) — architecture, deployment, and contribution guide

---

## 🧰 Tech Stack

| Component | Technology |
|-----------|-----------|
| UI Framework | Streamlit ≥ 1.56.0 |
| Computation | NumPy ≥ 2.4.4 |
| Visualisation | Matplotlib ≥ 3.10.8 |
| Scientific | SciPy ≥ 1.17.1 |
| Authentication | bcrypt ≥ 4.3.0 |
| Database | SQLite 3 (built-in) |
| Language | Python 3.10+ |

---

## 🔐 Security Features

| Feature | Implementation |
|---------|---------------|
| Password hashing | bcrypt with configurable rounds (default: 12) |
| Password strength | Configurable complexity rules (upper, lower, digit, special) |
| Session management | UUID tokens with idle timeout (default: 30 min) |
| Concurrent session limit | Max sessions per user (default: 3); oldest auto-invalidated |
| Account lockout | Configurable max failed attempts (default: 5) + lock duration (default: 15 min) |
| Login rate limiting | Sliding-window rate limiter per identifier (default: 10 / 60 s) |
| Signup rate limiting | Global sliding-window limiter (default: 5 / 60 s) |
| Input sanitization | HTML escaping, control-char removal, length enforcement on all user inputs |
| Log-injection prevention | Newlines and control characters stripped before writing to audit log file |
| Admin self-guard | Admins cannot deactivate or demote their own account |
| Simulator error boundary | Graceful degradation with typed error messages on module load failure |
| Audit trail | Every login, logout, signup, simulator access, and admin action logged |
| Input validation | Username format, email format, password minimum length |
| Role-based access | Student, Teacher, Admin roles with UI gating |
| Parameterised SQL | All database queries use parameter binding (no string interpolation) |

---

## ⚙️ Configuration

All settings are loaded from environment variables with sensible defaults.
See [`.env.example`](.env.example) for the full list.

| Variable | Default | Description |
|----------|---------|-------------|
| `STEMLAB_SECRET_KEY` | `change-me-in-production` | Session signing key |
| `STEMLAB_DATABASE_URL` | `data/stemlab.db` | SQLite database path |
| `STEMLAB_BCRYPT_ROUNDS` | `12` | Password hashing rounds |
| `STEMLAB_SESSION_TIMEOUT` | `1800` | Session idle timeout (seconds) |
| `STEMLAB_MAX_LOGIN_ATTEMPTS` | `5` | Failed logins before lockout |
| `STEMLAB_LOGIN_LOCK_SECONDS` | `900` | Lockout duration (seconds) |
| `STEMLAB_RATE_LIMIT_WINDOW` | `60` | Rate-limit sliding window (seconds) |
| `STEMLAB_RATE_LIMIT_MAX_LOGIN` | `10` | Max login attempts per window |
| `STEMLAB_RATE_LIMIT_MAX_SIGNUP` | `5` | Max signups per window |
| `STEMLAB_MAX_SESSIONS` | `3` | Concurrent sessions per user |
| `STEMLAB_PW_REQUIRE_UPPER` | `1` | Require uppercase in password |
| `STEMLAB_PW_REQUIRE_LOWER` | `1` | Require lowercase in password |
| `STEMLAB_PW_REQUIRE_DIGIT` | `1` | Require digit in password |
| `STEMLAB_PW_REQUIRE_SPECIAL` | `0` | Require special character in password |
| `STEMLAB_LOG_LEVEL` | `INFO` | Logging level |
| `STEMLAB_SUPPORT_EMAIL` | `advith.addaguduru@gmail.com` | Contact email |

---

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).

---

*Built with ❤️ for students and educators worldwide. v5.2 — Apache License 2.0*

