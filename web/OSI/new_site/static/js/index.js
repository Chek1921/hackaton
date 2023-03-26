const readMoreBtn = document.querySelector(".read_more");
const hiddenContent = document.querySelector(".hidden");

const animItems = document.querySelectorAll("._anim-items");


/* --------Read more animation------- */

readMoreBtn.addEventListener('click', () => {
  hiddenContent.classList.toggle('show');
  if (readMoreBtn.innerHTML === 'Читать далее') {
    readMoreBtn.innerHTML = 'Скрыть';
  } else {
    readMoreBtn.innerHTML = 'Читать далее';
  }
});
// -----------------------------------

/* --------Animation Scroll-------- */

if (animItems.length > 0) {
    window.addEventListener("scroll", animOnScroll);
    function animOnScroll() {
        for (let index = 0; index < animItems.length; index++) {
            const animItem = animItems[index]
            const animItemHeight = animItem.offsetHeight;
            const animItemOffset = offset(animItem).top;
            const animStart = 4;

            let animItemPoint = window.innerHeight - animItemHeight / animStart;

            if (animItemHeight > window.innerHeight) {
                animItemPoint = window.innerHeight - window.innerHeight / animStart;
            }

            if ((pageYOffset > animItemOffset - animItemPoint) && pageYOffset < (animItemOffset + animItemHeight)) {
                animItem.classList.add("_active");
            } else {
                if (!animItem.classList.contains("_anim-no-hide")) {
                    animItem.classList.remove("_active");
                }
            }
        }
    }

    function offset(el) {
        const rect = el.getBoundingClientRect(),
            scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
            scrollTop = window.pageYOffset ||  document.documentElement.scrollTop;
        return { top: rect.top + scrollTop, left: rect.left + scrollLeft}
    }
    setTimeout(() => {
        animOnScroll();
    }, 300)
}

// -----------------------------------

/* -------------Accordion ----------*/
const benefits = document.querySelectorAll(".benefits");

benefits.forEach((benefit) => {
    benefit.addEventListener("click", () => {
        benefit.classList.toggle("active");
    })
})

// -----------------------------------


// ------smooth scrolling-------
const anchors = document.querySelectorAll("footer a[href*='#']");

for (let anchor of anchors) {
    if (anchor) {
        anchor.addEventListener("click", function(e) {
            e.preventDefault();
            let anchorId = this.getAttribute("href");
            console.log(anchorId);
            document.querySelector(anchorId).scrollIntoView({
                behavior: "smooth",
                block: "start"
            })
        })
    }
}

// ---------------------------