const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Enable WebSocket interception
  await page.setRequestInterception(true);

  // Handle WebSocket connections
  page.on('webSocketCreated', (webSocket) => {
    console.log('WebSocket created:', webSocket.url());
    webSocket.on('frame', (data) => {
      console.log('WebSocket frame:', data);
    });
  });

  // Navigate to s0urce.io
  await page.goto('https://s0urce.io');

  // Scrape data from the page
  const data = await page.evaluate(() => {
    const elements = document.querySelectorAll('.data-item');
    const items = [];
    elements.forEach((element) => {
      const item = {
        title: element.querySelector('.title').textContent,
        description: element.querySelector('.description').textContent,
        link: element.querySelector('a').getAttribute('href'),
        data: JSON.parse(element.querySelector('.data').textContent),
      };
      items.push(item);
    });
    return items;
  });

  console.log(data);

  await browser.close();
})();
