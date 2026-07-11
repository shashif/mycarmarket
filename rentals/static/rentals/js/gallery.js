/* ==========================================
MyCarMarket Australia
Version: v2.0.1
File: rentals/static/rentals/js/gallery.js
Description:
Rental Image Gallery
========================================== */


/* ==========================================
SECTION 1 START
Change Main Image
========================================== */

function changeRentalImage(
    imageUrl,
    imageAlt,
    selectedButton
) {

    const mainImage = document.getElementById(
        "rental-main-gallery-image"
    );

    if (!mainImage) {

        return;

    }

    mainImage.src = imageUrl;

    mainImage.alt = imageAlt;


    document
        .querySelectorAll(
            ".rental-thumbnail-button"
        )
        .forEach(function(button) {

            button.classList.remove(
                "active"
            );

        });


    if (selectedButton) {

        selectedButton.classList.add(
            "active"
        );

    }

}


/* ==========================================
SECTION 1 END
Change Main Image
========================================== */


/* ----------------------------------------- */


/* ==========================================
SECTION 2 START
Keyboard Navigation
========================================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const thumbnails = document.querySelectorAll(
            ".rental-thumbnail-button"
        );

        thumbnails.forEach(function (
            thumbnail,
            index
        ) {

            thumbnail.addEventListener(
                "keydown",
                function (event) {

                    if (
                        event.key === "ArrowRight"
                    ) {

                        event.preventDefault();

                        const next =
                            thumbnails[
                                (index + 1) %
                                thumbnails.length
                            ];

                        next.focus();

                    }

                    if (
                        event.key === "ArrowLeft"
                    ) {

                        event.preventDefault();

                        const previous =
                            thumbnails[
                                (
                                    index -
                                    1 +
                                    thumbnails.length
                                ) %
                                thumbnails.length
                            ];

                        previous.focus();

                    }

                }
            );

        });

    }
);


/* ==========================================
SECTION 2 END
Keyboard Navigation
========================================== */