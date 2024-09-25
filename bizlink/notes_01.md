- if pip install jazzmine fails, use pip install django-jazzmin.
  - The latter is trying to install directly from PyPI (Python Package Index).
- translateY(-50%) moves the element vertically up by 50% of its own height. If the element has a height of 4px, it will be shifted up by 2px (which is 50% of 4px).
- translateX(-50%) moves the element horizontally left by 50% of its own width. If the element has a width of 100px, it will be shifted left by 50px (which is 50% of 100px).
- counter-reset: step;: Starts a counter named step at 1. You can set a different initial value by doing counter-reset: step 2 (here the counter starts at 3) (Note that this must be applied to a parent elemnt like flex contianer - an item with only one occurance)
- counter-increment: step;: Increases the step counter by 1 each time it's used.
  - counter-increment: step 1 increases teh step by 2. (Note that this must be appleid to child elements that can be counted like flex items - items with multiple occurance)
- content: counter(step);: Displays the current value of the step counter. (Note that this must be appleid to child elements that can be counted like flex items - items with multiple occurance)
- The CSS property transform-origin: top; sets the point around which an element will be transformed when using CSS transformations (like scale, rotate, animation, or translate).
- .account-item:hover .account-submenu: This selector targets any .account-submenu elements that are descendants (child or further nested child of child but must have the same class name) of .account-item class when .account-item is hovered over.
  - .account-item:hover > .account-submenu: This selector targets only direct child .account-submenu elements of .account-item when .account-item is hovered over.
- visibility: hidden, element still occupies spies, u can't interact with it, display: hidden - the element doesn't occupy space and u can't itnereact with it. Opcaity: 0 - teh element occupacies space and u can interact with it.
- The opposite of on_delete=models.CASCADE in foreignKey is on_delete=models.SET_NULL, null=True
- by default, Django sets both blank=False and null=False for TextField and most other field types.
- CharField alaways expects max_length as an attribute or else you will get an error.
- If you are using ShortUUID to generate unique ids for models in django, you may first be unable to make migrations. To fix that, remove teh unique attribute from teh lines of code that use the ShortUUID and then migrate. After that incldue and then migrate. That will fix it.
- to center absolute element relative to teh relative element horizontally do thsi: left: 50%; transform: translateX(-50%);
- to center absolute element relative to teh relative element vertically do this: top: 50% transform: translateY(-50%);
- suppose a container holds an image, if you set max-height or widht or min-height or width on teh image, then styles like width: 100% height: 100% and object-fit cover or container won't work properly becasue the contianer is restricting its own dimension and the image will overflow. To fix it, one method would be to use overflow: hidden, another is to not use max and min and just set the height and width attribute of teh cotnianer holding the image.
- suppose a contianer contianes another contianer. if u set the heigth of teh outer container and give the inner contianer a height greater than the height of the outer contianer, the inner continaer will overflow and the outer container won't grow to fit the inner container.
- {{ 123.456|floatformat }} → "123.5"
- {{ 123.0|floatformat }} → "123"
- {{ 123.456|floatformat:"2" }} → "123.46"
- {{ 123.4|floatformat:"3" }} → "123.400"
- {{ 1234.567|floatformat:"-2" }} → "1200"
- floatformat is only meant to be used in django templates and not models and views.
- you cannot use {{ ... }} within an {% if %} statement in Django templates like this: {% if {{ product.get_percentage|floatformat:"2" }} >= 100 %}
- In Django templates, comparison operators like < cannot be used directly with filtered values (e.g., |floatformat). The floatformat filter is applied after the value has already been used in the comparison, making the comparison ineffective. To solve this, you should compare the raw, unfiltered value (i.e., product.get_percentage) and then use floatformat only when displaying the value.
- When using position: absolute, the element is positioned relative to its nearest positioned ancestor, and it does not inherently include the padding of its container. This means that any padding applied to the container does not affect the positioning of the absolutely positioned element. It will position based on teh width of the element. Not that a position absolute requires a position relative on its parent element not another child element. If not provided then, it will position relative to its parent element, regardless.
- Note that if your url path passes an argument like id like this path("home/<categoryId>/"), the view function must use this same argument exactly like this def index(request, categoryId)
- If your context processor is passing categories = Category.objects.all() to all templates, this data will be available globally across your site. If a specific view needs to pass a filtered set of categories (e.g., categories = Category.objects.filter(published=True)) to its template, this is done explicitly in the view function.
  - Data passed from views to templates will always take precedence over data provided by context processors. So if your template requires specific categories filtered by the view, those will be used, and the global context processor data won’t interfere.
- if u place 5 lists inside 1 div, each list will be one div. if u apply flex on teh div to make teh lists a row, it won't work. U need to flex the parent of this div to make this functionality work.
- align-content-center on a block level container will center any content inisde it horizontally and verticlaly.
- if you are applying border radius on a button but the button isn't showing it althought the border around it does show it, chnage the background color of the button. It will work. Usually this happens when the bootstrap default classes such as btn-primary are applied. chnage teh background of the button remove teh btn primary and it should work.
- on an image element if u set width: 100% and heigth 100%
- if you add object-fit: cover, the object will take all the width and height provided, unless u set max or min widht and height on the contianer holding the image in which case, teh iage isnide will overflow
- if you add object-fit: contain, the image will take the widht and height that fit its actual width and height. In that attempt, the object may cover the whole contianer and get cropped or it may fit inside teh container and cover only a few space.
- If you put the closing tag of textarea tag on a new line, the text inisde won't start from teh beginning. Instead, it will start somewhere at teh middle. You won't detect this space in dev tools because it is not padding.
- A ForeignKey represents a one-to-many relationship. Hence, if an item model is an attribute to a featured item model using a foreign key, then one item can be referenced many times at different time and place. Each featured item can point to only one specific item with s specific id.
- By default, <ul> elements have block-level behavior and their child <li> elements stack vertically. Using display-flex on the ul element won't necessarly put the li elements in row by default. This is because list-specific styling (like list-style-type and margin/padding) can interfere. To fix such issue, you are going to have to explicitely set the flex-direciton to row.
  - Such cases usually occur when u use the bootstrap list-group and list-group-item
- z-index only works on elements with a positioning context, such as position: relative, position: absolute, or position: fixed. If an element doesn't have position defined, it won’t respect z-index rules.
- to increase teh width of a bootstrap modal, use max-width and not width or min-width on the modal dialogue and make width: 100% for the modal-content
- the usage of .all() is appropriate only for fields like ManyToManyField or reverse ForeignKey relationships
- you can do "{% if forloop.first %}" to get the first item in for loop in django
- Swiper needs to clone slides for the loop functionality.
  - if slides number is slidesperview + 1, the right click of the swiper will only be clickable once. It works for all oter cases
  - such scenario makes it not ideal to use swiper package for creating image sliders. Use it only when the slides are not dynamic. that way you can adjust the slides perview so that it is at least 2 less than the total number of slides.
- data-bs-ride="carousel": This attribute automatically initializes the carousel to start cycling through items as soon as the page loads.
- Bootstrap’s JavaScript automatically applies a default interval of 5000 milliseconds (5 seconds) between slides unless specified otherwise with data-bs-interval.
- When creating a js script that interacts with the DOM. like an image slider, it is better to defien the code in a script tag at the end of the html file. Defining the code in an external js file and then extedning that won't work properly.
- Assigning height and/or width to a container won't allow it to grow with the contents that are inside of it. Instead, the contents inside will overflow outside.
- The <source> tag inside the <video> element is used to specify multiple media resources (such as different video formats) for the browser to choose from. This ensures cross-browser compatibility, as not all browsers support the same video formats natively.
  - It is better to use teh video tag and inside it pass the src to teh source tag instead of using teh video tag and directly passing the src attribute to the video tag.
    - The controls attribute on teh video tag adds play/pause buttons and other video controls.
  - On a flex item, if u set the width to 100%, it will grow to occupy the width of the felx container.
- The video tag isn't like the image tag. The best way to resize an image would be to define width and height values ont he container and then pass 100% to the width and height for the video tag.
  - If you try to define height and width directly on the video tag, then teh image will resize to one of the two and it will adjust the other based on the best choice for that resolution.
- align-content center is applied on a block level elemtn that u want centerd. it is applied directly on the element to be centered not is parent element.
- these are attributes that you can pass to the video tag "autoplay muted loop"
- For the selector video:hover + i: It means "select the <i> element that directly follows a <video> element when that <video> is being hovered over."
  - If you have two elements (like <video> and <i>) within the same parent (like a <div>), the adjacent sibling combinator (+) will only select the <i> if it comes immediately after the <video>.
- video:hover i {} - targets and icon element in teh video tag. video:hover + i {} - targets an icon element that si directly below the video tag.
- The selector video > i targets any <i> element that is a direct child of a <video> element. It will only apply styles to an <i> that is directly nested inside the <video>, with no other elements in between. video i: This selector targets all <i> elements that are descendants of a <video> element, regardless of how deep they are nested. This means it will apply styles to any <i> inside the <video>, even if it is wrapped in other elements.
-                 /* Style to hide the scroll bar on chrome, safari and opera */
                .more-video::-webkit-scrollbar {
                    display: none;
                }

                /* Style to hide the scroll bar on IE, edge and firefox */
                .more-video::-webkit-scrollbar {
                    -ms-overflow-style: none;
                    scroll-behavior: none;
                }
