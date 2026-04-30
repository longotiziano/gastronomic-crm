# Tables

## Search
Every table div has a brother input element with class `searcher`. This allows the search to be recognizable.

## Datasets
- `tablemodel`: comented below
- `endpoint`: the HTTP GET endpoint for the table's data

## Columns recognition
The function knows which columns display based on the `config.json` file and the dataset of the table.

For example, in html:
```html
<div class="table" data-tablemodel="products"></div>
```
In config.json
```json
{
    "models": {
        "products": {
            "cols": [],
            "cols_displayed": ["product_name", "product_category", "price"],
            "..."
        }
    }
}
```

And in JS
```js
import { configData } from './config.json';
const cols = configData.models.dataset.tablemodel.cols_displayed;
```