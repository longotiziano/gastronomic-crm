# Buttons

## Selectables
The selectables' class always have a `<ul>` father, and each `<li>` will have a button. If there's more than one button, then the user is allowed to choose just one for each `<ul>`.

Also, the data gained from these will be normally displayed in the URL. These classes are generalizated.

### Considerations
To work with this class, the `<ul>` mentioned should contain a data parameter named `data-name=<name>` and in the buttons `<data-<name>=<value>>`

For example:
```html
<ul data-name=restaurant class=selectables>
    <li><button data-restaurant=club_serrano>Club Serrano</button></li>
    <li><button data-restaurant=kubo>Kubo</button></li>
</ul>
```
This allows the functions to be reutilized in JavaScript.

## Actionables

## Uploaders
I designed a upload button that have this structure:
```html
<div class="upload" data-uploaderid="<id_example>">
    <input type="file" id="<id_example>">
    <div class="actionable">
        <div style="visibility: hidden">    
            <span>Archivo seleccionado</span>
            <svg>...</svg>
        </div>
        <svg style="visibility: visible; position: absolute;">...</svg>
    </div>
    <button class="actionable">Subir archivo</button>    
</div>
```
The only thing that you should change is the `data-uploaderid` attribute depending on the input's id.