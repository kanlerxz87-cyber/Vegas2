#!/usr/bin/env node
// Exercise the dependency-free dining filter script with a tiny DOM mock.
const fs = require("node:fs");
const vm = require("node:vm");
const assert = require("node:assert/strict");

const cards = [
  { textContent: "China Poblano · Chinese Mexican", dataset: { michelin: "bib" }, hidden: false },
  { textContent: "Joël Robuchon · French", dataset: { michelin: "star" }, hidden: false },
  { textContent: "Bouchon · French bistro", dataset: { michelin: "listed" }, hidden: false },
];
const inputHandlers = {};
const buttons = ["all", "stars", "bib", "listed"].map((filter) => ({
  dataset: { restaurantFilter: filter },
  attrs: {},
  handlers: {},
  setAttribute(name, value) { this.attrs[name] = value; },
  addEventListener(event, handler) { this.handlers[event] = handler; },
}));
const input = { value: "", addEventListener(event, handler) { inputHandlers[event] = handler; } };
const resultCount = { textContent: "" };

global.document = {
  querySelector(selector) {
    if (selector === "#restaurant-search") return input;
    if (selector === "#restaurant-result-count") return resultCount;
    return null;
  },
  querySelectorAll(selector) {
    if (selector === "[data-restaurant-card]") return cards;
    if (selector === "[data-restaurant-filter]") return buttons;
    return [];
  },
};

vm.runInThisContext(fs.readFileSync("site/session-b29fc34e/assets/js/site.js", "utf8"), { filename: "site/session-b29fc34e/assets/js/site.js" });
assert.equal(resultCount.textContent, "3 of 3 restaurants shown");
input.value = "poblano";
inputHandlers.input();
assert.equal(resultCount.textContent, "1 of 3 restaurants shown");
assert.equal(cards[0].hidden, false);
assert.equal(cards[1].hidden, true);
buttons.find((button) => button.dataset.restaurantFilter === "bib").handlers.click();
assert.equal(resultCount.textContent, "1 of 3 restaurants shown");
assert.equal(buttons.find((button) => button.dataset.restaurantFilter === "bib").attrs["aria-pressed"], "true");
buttons.find((button) => button.dataset.restaurantFilter === "stars").handlers.click();
assert.equal(resultCount.textContent, "0 of 3 restaurants shown");
console.log("Dining search and MICHELIN filters passed.");
