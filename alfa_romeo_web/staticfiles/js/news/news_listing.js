
document.addEventListener('DOMContentLoaded', function () {
    const ourDomSelectors = {
        mainNewsContainer: document.querySelector('.news-cards-container'),
        paginationContainer: document.getElementById('pagination')
    }

    let currentPage = 1;
    let itemsPerPage = 3;  // Hardcoded, TODO: handle it better

    function fetchNews(page) {
        fetch(`/news/api/?page=${page}`)
            .then(response => response.json())
            .then((data) => {

                data.results.forEach(info => {
                    console.log(info)
                    let newDiv = createElement('div', ourDomSelectors.mainNewsContainer, '', ['news-card']);
                    createElement('h2', newDiv, `${info.title}`);
                    if (info.img_field) {
                        console.log('Image field:', info.img_field);
                        let imgDiv = createElement('div', newDiv, '', ['image-container']);
                        let imgElement = createElement('img', imgDiv, '', ['news-image']);
                        imgElement.src = info.img_field;
                        imgElement.alt = info.title + ' image';
                    }
                    let description = info.description.slice(0, 300);
                    if (info.description.length > 300) {
                        description += '...';
                    }
                    createElement('p', newDiv, description);

                    let articleLink = createElement('a', newDiv, 'Read Article');

                    articleLink.href = `details/${info.slug}`;
                })

                generatePaginationLinks(data.count, itemsPerPage);
            })
            .catch((err) => console.log(err))
    }

    fetchNews(currentPage);

    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('pagination-link')) {
            currentPage = parseInt(event.target.dataset.page);
            ourDomSelectors.mainNewsContainer.innerHTML = '';
            fetchNews(currentPage);
        }
    });

    function generatePaginationLinks(totalCount, itemsPerPage) {
    ourDomSelectors.paginationContainer.innerHTML = '';

        const totalPages = Math.ceil(totalCount / itemsPerPage);

        if (currentPage > 1) {
            let prevLi = createElement('li', ourDomSelectors.paginationContainer);
            let prevLink = createElement('a', prevLi, '', ['pagination-link', 'fa-solid', 'fa-angles-left']);
            prevLink.dataset.page = currentPage - 1;
        }

        for (let i = 1; i <= totalPages; i++) {
            let li = createElement('li', ourDomSelectors.paginationContainer);
            let link = createElement('a', li, i.toString(), ['pagination-link']);
            link.dataset.page = i;

            if (i === currentPage) {
                link.classList.add('current-page');
            }
        }

        if (currentPage < totalPages) {
            let nextLi = createElement('li', ourDomSelectors.paginationContainer);
            let nextLink = createElement('a', nextLi, '', ['pagination-link', 'fa-solid', 'fa-angles-right']);
            nextLink.dataset.page = currentPage + 1;
        }
    }

    function createElement(type, parentNode, content, classes, id, attributes, useInnerHtml) {
        const htmlElement = document.createElement(type)

        if (content && useInnerHtml) {
            htmlElement.useInnerHtml = content;
        } else {
            if (content && type !== 'input') {
                htmlElement.textContent = content;
            }

            if (content && type === 'input') {
                htmlElement.value = content
            }
        }

        if (classes && classes.length > 0) {
            htmlElement.classList.add(...classes);
        }

        if (id) {
            htmlElement.id = id
        }

        if (attributes) {
            for (const key in attributes) {
                htmlElement[key] = attributes[key]
            }
        }

        if (parentNode) {
            parentNode.appendChild(htmlElement)
        }

        return htmlElement
    }

});