function changeMainImage(imageUrl) {
    const mainImage = document.getElementById('mainCarImage');

    if (mainImage) {
        mainImage.src = imageUrl;
    }
}