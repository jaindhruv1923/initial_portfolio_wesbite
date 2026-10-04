<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:1B1B2F,100:C9971F&height=180&section=header&text=GRILLI&fontSize=58&fontColor=E6E8EF&animation=fadeIn&fontAlignY=38&desc=Restaurant%20Website%20%2B%20Live%20Reservation%20System&descAlignY=58&descSize=20)

<a href="#">
  <img src="https://readme-typing-svg.demolab.com?font=IBM+Plex+Mono&size=18&duration=3000&pause=1200&color=C9971F&center=true&vCenter=true&width=650&lines=Static+template+%E2%86%92+full-stack+reservation+system;Node.js+%2B+Express+REST+API+%C2%B7+5+endpoints;MongoDB-backed+booking+persistence;6+bugs+fixed+%C2%B7+1+new+section+built+from+scratch;%22Our+Chefs%22+%E2%80%94+custom-built%2C+not+part+of+the+template" alt="Typing SVG" />
</a>

<br/>

[![Node.js](https://img.shields.io/badge/Node.js-Backend-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org/)
[![Express](https://img.shields.io/badge/Express.js-REST_API-000000?style=for-the-badge&logo=express&logoColor=white)](https://expressjs.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Reservation_Store-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](#)
[![License](https://img.shields.io/badge/License-MIT-2F7D4F?style=for-the-badge)](LICENSE)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jaindhruv1923)
[![Email](https://img.shields.io/badge/Email-Reach_Out-C9971F?style=for-the-badge&logo=gmail&logoColor=white)](mailto:jaindhruv1923@gmail.com)

**Built by [Dhruv Jain](https://github.com/jaindhruv1923)** · B.Tech CSE (AI & Data Science), BML Munjal University

</div>

<br/>

## 📖 Table of Contents

- [What this is](#-what-this-is)
- [Key results](#-key-results)
- [Screenshots](#-screenshots)
- [Architecture](#-architecture)
- [What's inside](#-whats-inside)
- [Reservation API](#-reservation-api)
- [Tech stack](#-tech-stack)
- [Quickstart](#-quickstart)
- [Repo structure](#-repo-structure)
- [Honest limitations](#-honest-limitations)
- [Roadmap](#-roadmap)
- [Connect](#-connect)

<br/>

## 🎯 What this is

> Grilli started as a **static restaurant landing page template** — good-looking
> frontend, but a reservation form that didn't actually submit anywhere and a
> handful of broken internal links. This project turns it into a **working
> full-stack product**: a real Node.js + Express REST API, a MongoDB-backed
> reservation store, and a brand-new "Our Chefs" section that didn't exist in
> the original template at all.

The goal wasn't to redesign the frontend from scratch — it was to take a
template that *looked* production-ready and make it actually behave like one:
fix what was broken, wire the form to a real backend, and add a section the
original was missing.

<br/>

## 🏆 Key results

<div align="center">

| Area | Result |
|:---|:---:|
| 🐛 **Template bugs fixed** | ![Bugs](https://img.shields.io/badge/6_bugs_fixed-broken_links_%2B_dead_form-C9971F?style=flat-square) |
| 🧑‍🍳 **New section built** | ![Section](https://img.shields.io/badge/%22Our_Chefs%22-built_from_scratch-2F7D4F?style=flat-square) |
| 🔌 **REST API** | ![Endpoints](https://img.shields.io/badge/5_endpoints-Node.js_%2B_Express-339933?style=flat-square) |
| 🗄️ **Database** | ![DB](https://img.shields.io/badge/MongoDB-reservation_persistence-47A248?style=flat-square) |

</div>

<br/>

## 📸 Screenshots

**🏠 Homepage — Hero**

<p align="center"><img src="preview_intro.png" width="85%"/></p>
<p align="center"><i>"Where every flavor tells a story" hero slide with top nav and "Find a Table" CTA</i></p>

<br/>

**📖 Our Story**

<p align="center"><img src="our_story.png" width="85%"/></p>
<p align="center"><i>About section — story, gallery collage, and "Since 1950" badge</i></p>

<br/>

**🍽️ We Offer Top Notch**

<p align="center"><img src="what_we_offer.png" width="85%"/></p>
<p align="center"><i>Breakfast / Appetizers / Drinks category highlights</i></p>

<br/>

**📋 Delicious Menu**

<p align="center"><img src="menu.png" width="85%"/></p>
<p align="center"><i>Menu preview with pricing pulled from the template's menu data</i></p>

<br/>

**🧑‍🍳 Our Chefs** — *built from scratch, not part of the original template*

<p align="center"><img src="our_chefs.png" width="85%"/></p>
<p align="center"><i>New "Meet the Team" section added on top of the existing design language</i></p>

<br/>

**📅 Reservation Form — Live Submission**

<p align="center"><img src="online_reservation.png" width="85%"/></p>
<p align="center"><i>Reservation form successfully submitting to the Express API — "Table booked successfully!" confirmation shown</i></p>

<br/>

**🗄️ Stored Reservation — MongoDB Atlas**

<p align="center"><img src="db-record.png" width="85%"/></p>
<p align="center"><i>The submitted reservation persisted as a real document in the <code>reservations</code> collection on Atlas — name, phone, guests, date, time, message, and status all saved correctly</i></p>

<br/>

**⚓ Footer**

<p align="center"><img src="footer.png" width="85%"/></p>
<p align="center"><i>Footer with contact details, newsletter subscribe, and social links</i></p>

<br/>

## 🏗️ Architecture

```mermaid
flowchart LR
    U["🧑 Visitor"] --> FE["🖥️ Frontend\nHTML / CSS / JS"]
    FE -- "Reservation form submit" --> API["🔌 Express REST API\n5 endpoints"]
    API --> DB[("🗄️ MongoDB\nreservations collection")]
    API --> FE

    style FE fill:#1B1B2F,color:#fff
    style API fill:#000000,color:#fff
    style DB fill:#47A248,color:#fff
```

<br/>

## 📦 What's inside

| Part | What it does |
|---|---|
| 🏠 **Landing page** | Menu, gallery, testimonials, about — from the original template |
| 🧑‍🍳 **Our Chefs** | New section built from scratch — not present in the original template |
| 📅 **Reservation form** | Frontend form wired to the new backend (was a dead submit handler before) |
| 🔌 **Express API** | 5 REST endpoints handling reservation create/read/update logic |
| 🗄️ **MongoDB store** | Persists every reservation submitted through the form (verified live on Atlas) |

<br/>

## 🔌 Reservation API

<details>
<summary><b>Click to expand — replace with your actual route list before publishing</b></summary>
<br/>

The backend exposes 5 REST endpoints for the reservation flow. Fill in the
exact routes from your `routes/` folder — for example:

| Method | Route | Purpose |
|---|---|---|
| `POST` | `/api/reservations` | Create a new reservation |
| `GET` | `/api/reservations` | List all reservations |
| `GET` | `/api/reservations/:id` | Get a single reservation |
| `PUT` | `/api/reservations/:id` | Update a reservation |
| `DELETE` | `/api/reservations/:id` | Cancel a reservation |

*(Update this table to match the actual routes in your codebase — don't leave
placeholder paths in the final version.)*

</details>

<br/>

## 🛠️ Tech stack

<div align="center">

| Layer | Tools |
|---|---|
| **Frontend** | HTML5 · CSS3 · JavaScript |
| **Backend** | Node.js · Express.js |
| **Database** | MongoDB Atlas |
| **API style** | REST — 5 endpoints |
| **Base template** | [Grilli by codewithsadee](https://github.com/codewithsadee/grilli) (frontend only — backend is original work) |

</div>

<br/>

## 🚀 Quickstart

```bash
# Clone the repo
git clone https://github.com/jaindhruv1923/<grilli-repo-name>.git
cd <grilli-repo-name>

# Install backend dependencies
cd backend
npm install

# Set up environment variables
cp .env.example .env
# Add your MongoDB connection string to .env

# Run the server
npm start
```

Then open the frontend in your browser (or serve it via a static file server)
and submit a test reservation to confirm it's saved in MongoDB.

<br/>

## 📁 Repo structure

```
grilli/
├── frontend/                # Static site — HTML, CSS, JS
│   ├── index.html
│   ├── assets/
│   └── ...
├── backend/                 # Express server + API routes
│   ├── server.js
│   ├── routes/
│   │   └── reservations.js
│   ├── models/
│   │   └── Reservation.js
│   └── ...
├── .env.example
├── LICENSE
└── README.md
```

*(Update this to match your actual folder layout — don't leave it generic in
the final version.)*

<br/>

## ⚠️ Honest limitations

- The reservation system does **not** send confirmation emails/SMS — it only
  persists the booking to MongoDB.
- No admin dashboard yet — reservations are stored but not visualized or
  manageable from a UI.
- No authentication — the API currently has no protection against spam
  submissions.
- Base frontend design is from the [codewithsadee Grilli template](https://github.com/codewithsadee/grilli); the "Our Chefs" section and the entire backend are original work.

<br/>

## 🗺️ Roadmap

- [ ] Add email/SMS confirmation on successful reservation
- [ ] Build a simple admin view to see/manage bookings
- [ ] Add basic rate-limiting / spam protection on the API
- [x] Fix all broken links and the dead reservation form
- [x] Build "Our Chefs" section from scratch
- [x] Build working Express + MongoDB backend

<br/>

## 📫 Connect

<div align="center">

Open to Data Analyst / Business Analyst roles and collaborations — feel free to reach out.

<a href="https://github.com/jaindhruv1923">
  <img src="https://img.shields.io/badge/GitHub-Project_Repo-181717?style=for-the-badge&logo=github&logoColor=white" />
</a>
<a href="https://www.linkedin.com/in/jaindhruv1923">
  <img src="https://img.shields.io/badge/LinkedIn-jaindhruv1923-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>
<a href="mailto:jaindhruv1923@gmail.com">
  <img src="https://img.shields.io/badge/Email-jaindhruv1923@gmail.com-C9971F?style=for-the-badge&logo=gmail&logoColor=white" />
</a>

</div>

<br/>

<div align="center">

**[Dhruv Jain](https://github.com/jaindhruv1923)** · [LinkedIn](https://www.linkedin.com/in/jaindhruv1923) · [jaindhruv1923@gmail.com](mailto:jaindhruv1923@gmail.com)

![footer](https://capsule-render.vercel.app/api?type=waving&color=0:1B1B2F,100:C9971F&height=100&section=footer)

</div>
