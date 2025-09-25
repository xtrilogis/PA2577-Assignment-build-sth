const express = require("express");
const { createProxyMiddleware } = require("http-proxy-middleware");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;


app.use(express.static(path.join(__dirname, "public")));

// Proxy API calls to FastAPI service inside the cluster
app.use(
  "/items", // dev: /test/items/
  createProxyMiddleware({
    target: "http://fast-api-svc:8000",
    changeOrigin: true,
  })
);

app.listen(PORT, () => {
  console.log(`Express server running on port ${PORT}`);
});
