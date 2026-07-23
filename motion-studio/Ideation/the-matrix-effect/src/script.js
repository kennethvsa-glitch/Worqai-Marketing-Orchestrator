// for loop to creat the vertical lines 
for (let i = 0; i < 75; i++) {
    const proxy = document.createElement("div");
    proxy.classList.add(`line-${i}`);
   $(proxy).css({
        "position": "relative",
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
        "color": "#1b6812",
        "font-size": "2rem",
        "mask-image": "linear-gradient(to top, black 50%, transparent 100%)",})
  
   const text = document.createTextNode('gdudtd1fkjdf4ldglfjdghsdf');
    proxy.appendChild(text);
    $(".matrix").append(proxy);
  
//gsap split text to char with class mcode
  var split = new SplitText(`.line-${i}`, { type: "chars", charsClass: "mcode" })
    const lines = split.chars;
  
   gsap.set(`.line-${i}`, { yPercent: -100 })
   const tn = gsap.timeline();
    tn.from(lines, { duration: 0.3, repeat: -1, yoyo: true, scrambleText: { chars: 'gdudtd12kjd34ldgl4340hsdf' }, ease: "power2.out" });

    const tl = gsap.timeline({ repeat: -1 });
    tl.to(`.line-${i}`, { duration: 5, delay: Math.random() * 10, yPercent: 100 })
}

$("#btn").on("click", () => {
    gsap.to('.matrix', { duration: 3, transformOrigin: "center", autoAlpha: 0, scale: 8, ease: "power2.out" })
    gsap.to('.btns', { duration: 0.3, scaleY: 0, scaleX: 2, ease: "power2.out" })
})

