const express = require('express');
const puppeteer = require('puppeteer');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(express.static('public'));  // Serve the static files (HTML, CSS)

app.post('/chat', async (req, res) => {
    const message = req.body.message;
    
    // Simulate a web scraping action (e.g., scrape a Google search result or Wikipedia)
    const reply = await scrapeWeb(message);

    // Send back the reply to the frontend
    res.json({ reply });
});

// Example of a simple web scraping function
async function scrapeWeb(query) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    // Scrape data (this example scrapes a Google search result)
    await page.goto(`https://www.google.com/search?q=${query}`);
    
    const result = await page.evaluate(() => {
        const firstResult = document.querySelector('.BVG0Nb');
        return firstResult ? firstResult.textContent : "Sorry, I couldn't find anything.";
    });
    
    await browser.close();
    return result;
}

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
