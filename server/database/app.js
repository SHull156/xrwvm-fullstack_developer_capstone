/* jshint esversion: 8 */

const express = require("express");
const mongoose = require("mongoose");
const fs = require("fs");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const port = 3030;

// Middleware
app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Load JSON data
const reviewsData = JSON.parse(fs.readFileSync("reviews.json", "utf8"));
const dealershipsData = JSON.parse(fs.readFileSync("dealerships.json", "utf8"));

// Mongoose connection
mongoose.connect("mongodb://mongo_db:27017/", { dbName: "dealershipsDB" });

// Import models
const Reviews = require("./review");
const Dealerships = require("./dealership");

// Populate database
(async () => {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviewsData.reviews);

    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealershipsData.dealerships);
  } catch (error) {
    console.error("Error populating database:", error);
  }
})();

// Routes

app.get("/", (req, res) => {
  res.send("Welcome to the Mongoose API");
});

app.get("/fetchReviews", async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching documents" });
  }
});

app.get("/fetchReviews/dealer/:id", async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching documents" });
  }
});

app.get("/fetchDealers", async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching documents" });
  }
});

app.get("/fetchDealers/:state", async (req, res) => {
  try {
    const documents = await Dealerships.find({ state: req.params.state });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching documents" });
  }
});

app.get("/fetchDealer/:id", async (req, res) => {
  try {
    const document = await Dealerships.findOne({ id: req.params.id });
    if (document) {
      res.json(document);
    } else {
      res.status(404).json({ error: "Dealer not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Error fetching document" });
  }
});

app.post("/insert_review", express.raw({ type: "*/*" }), async (req, res) => {
  try {
    const data = JSON.parse(req.body);
    const lastReview = await Reviews.find().sort({ id: -1 }).limit(1);
    const newId = lastReview.length > 0 ? lastReview[0].id + 1 : 1;

    const review = new Reviews({
      id: newId,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year,
    });

    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error inserting review" });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
