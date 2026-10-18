const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

const reviewsFile = fs.existsSync("reviews.json") ? "reviews.json" : "data/reviews.json";
const dealershipsFile = fs.existsSync("dealerships.json") ? "dealerships.json" : "data/dealerships.json";

const reviews_data = JSON.parse(fs.readFileSync(reviewsFile, 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync(dealershipsFile, 'utf8'));

const Reviews = require('./review');
const Dealerships = require('./dealership');

async function initDB() {
  const mongoUrl = process.env.MONGO_URL;
  if (mongoUrl) {
    await mongoose.connect(mongoUrl, { dbName: 'dealershipsDB' });
  } else {
    try {
      await mongoose.connect("mongodb://mongo_db:27017/", {
        dbName: 'dealershipsDB',
        serverSelectionTimeoutMS: 2000
      });
      console.log("Connected to MongoDB at mongodb://mongo_db:27017/");
    } catch (err) {
      console.log("Remote/Docker MongoDB not found. Starting in-memory MongoDB...");
      const { MongoMemoryServer } = require('mongodb-memory-server');
      const mongod = await MongoMemoryServer.create();
      const uri = mongod.getUri();
      await mongoose.connect(uri, { dbName: 'dealershipsDB' });
      console.log("Connected to in-memory MongoDB at", uri);
    }
  }

  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviews_data['reviews']);
    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealerships_data['dealerships']);
    console.log("Database initialized with reviews and dealerships data.");
  } catch (error) {
    console.error("Error initializing database data:", error);
  }
}

initDB();

// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get(['/fetchReviews/dealer/:id', '/fetchReviews/dealer'], async (req, res) => {
  try {
    const query = req.params.id ? { dealership: req.params.id } : {};
    const documents = await Reviews.find(query);
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const documents = await Dealerships.find({ state: req.params.state });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch dealer by a particular id
app.get(['/fetchDealer/:id', '/fetchDealer'], async (req, res) => {
  try {
    const query = req.params.id ? { id: req.params.id } : {};
    const documents = await Dealerships.find(query);
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  data = JSON.parse(req.body);
  const documents = await Reviews.find().sort( { id: -1 } );
  let new_id = documents[0]['id'] + 1;

  const review = new Reviews({
		"id": new_id,
		"name": data['name'],
		"dealership": data['dealership'],
		"review": data['review'],
		"purchase": data['purchase'],
		"purchase_date": data['purchase_date'],
		"car_make": data['car_make'],
		"car_model": data['car_model'],
		"car_year": data['car_year'],
	});

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
		console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
