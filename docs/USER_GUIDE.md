# 📖 STEM Lab — User Guide

Welcome to **STEM Lab**, an interactive educational platform for Physics, Chemistry, and Mathematics. This guide will help you get the most out of every simulator.

---

## Getting Started

### 1. Open the Platform

Visit the Streamlit Cloud deployment URL, or run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

### 2. Create an Account or Log In

On your first visit you'll see the **login / signup** screen.

- **Sign up** — provide a username, email, display name, and password.
- **Log in** — enter your username and password.

See [Account & Security](#account--security) below for password rules and lockout details.

### 3. Navigate

| Step | Action |
|------|--------|
| 1 | Click **🧪 Simulators** in the sidebar |
| 2 | Choose a **simulator pack** (Foundation, Core STEM, Advanced, or Cross-Disciplinary) |
| 3 | Pick a **subject** — Physics, Chemistry, Mathematics, or Applied STEM |
| 4 | Choose a **topic** to launch the interactive simulator |

### 4. Interact

- **Sliders** — drag to change continuous values (speed, angle, temperature, …).
- **Dropdowns** — pick from predefined options.
- **Radio buttons / tabs** — switch sub-topics within a simulator.
- **Number inputs** — type precise values.
- **Graphs** — update in real time as you change parameters.

---

## Account & Security

### Signing Up

| Field | Rules |
|-------|-------|
| Username | 3–30 characters, must start with a letter, letters/digits/underscores only |
| Email | Must be a valid email address (max 254 characters) |
| Display name | Up to 100 characters |
| Password | Minimum 8 characters. Must include at least 1 uppercase letter, 1 lowercase letter, and 1 digit. Maximum 128 characters |

> **Tip:** The platform enforces signup rate limiting. If you see a "too many signups" message, wait a minute and try again.

### Logging In

- Enter your **username** and **password**.
- After **5 consecutive failed attempts** your account is temporarily locked for 15 minutes.
- Login attempts are also rate-limited (max 10 per 60-second window).

### Sessions

| Behaviour | Default |
|-----------|---------|
| Idle timeout | 30 minutes — you'll be logged out automatically |
| Concurrent sessions | Maximum 3 — if you log in on a 4th device the oldest session is ended |
| Logout | Click the **Logout** button in the sidebar to end your session immediately |

All session and security limits are configurable by the platform administrator.

---

## Pack & Age Guide

| Pack | Age Range | Subjects | Simulators |
|------|-----------|----------|------------|
| 🔰 Foundation (Grades 6–8) | 11–14 | Physics, Chemistry, Mathematics | 14 |
| 🌍 Core STEM (Grades 9–10) | 14–16 | Physics, Chemistry, Mathematics | 16 |
| 🎓 Advanced (Grades 11–12) | 16–18 | Physics, Chemistry, Mathematics | 28 |
| 🧩 Cross-Disciplinary Enrichment | All ages | Applied STEM | 4 |

---

## Subjects

### 🔬 Physics

Covers mechanics, forces, energy, waves, electricity, light, sound, thermal physics, and oscillations across all grade levels.

### ⚗️ Chemistry

Covers states of matter, elements, bonding, reactions, equilibrium, kinetics, thermochemistry, and organic chemistry.

### 📐 Mathematics

Covers number patterns, geometry, statistics, trigonometry, coordinate geometry, algebra, functions, and calculus.

---

## Your Profile

Click **👤 Profile** in the sidebar to:

- View your account details (username, email, display name, role).
- **Change your password** — you must enter your current password and a new password that meets the strength rules above.
- Browse your **activity history** — a log of your recent logins, simulator visits, and other actions.

---

## Admin Dashboard

> This section applies only to users with the **Admin** role.

Click **⚙️ Admin** in the sidebar to access:

| Feature | Description |
|---------|-------------|
| User list | Search, filter, and view all registered accounts |
| Role management | Promote or demote users (Student / Teacher / Admin) |
| Account activation | Activate or deactivate user accounts |
| Audit log | Browse the full audit trail with action and date filters |
| Dashboard stats | User counts, recent activity, and action breakdowns |

> **Safety note:** Admins cannot deactivate or demote their own account to prevent accidental lockout.

---

## Tips for Effective Learning

1. **Change one variable at a time** — observe the effect before adjusting another.
2. **Try extreme values** — push sliders to their limits to understand boundary behaviour.
3. **Predict first, then check** — form a hypothesis before moving a slider.
4. **Cross-reference your textbook** — every equation displayed matches standard syllabi.
5. **Use reference links** — each simulator includes curated links to Khan Academy, PhET, BBC Bitesize, and other trusted sources. Click the pill-shaped links above the simulator to deepen your understanding.
6. **Take notes** — write down observations for revision.
7. **Use the formula** — each simulator shows the governing equation in LaTeX.

---

## Keyboard Shortcuts (Streamlit)

| Shortcut | Action |
|----------|--------|
| `R` | Re-run the app |
| `C` | Clear cache |
| `Ctrl + /` | Toggle sidebar |

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Graphs not rendering | Refresh the page (`Ctrl + R`) |
| Sidebar collapsed | Click the `>` arrow at the top left |
| Slow performance | Reduce the number of data points / trials |
| Import error | Run `pip install -r requirements.txt` || Account locked | Wait 15 minutes and try again, or ask an admin to unlock your account |
| Password rejected | Ensure it's 8+ characters with at least 1 uppercase, 1 lowercase, and 1 digit |
| "Too many attempts" | Rate limit reached — wait 60 seconds before retrying |
| Session expired | Your session timed out after 30 minutes of inactivity — log in again |
| Simulator error | The error boundary will display a message — try refreshing or contact support |
---

## Legal Pages

The sidebar includes links to:

- **Terms of Service** — usage rules and acceptable-use policy.
- **Privacy Policy** — how your data is stored and protected.

---

## For Teachers

- Use the **Home page** stats to show students the breadth of available content.
- Assign specific simulators by sharing the URL with sidebar state.
- Ask students to **predict outcomes** before interacting, then verify.
- Use the **Statistics & Probability** simulator for live classroom demonstrations with random trials.
- Use the **Admin Dashboard** (if you have Teacher or Admin role) to monitor student activity via the audit log.

---

*STEM Lab · Apache License 2.0 · v5.2 · © 2026*
