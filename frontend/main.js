import data from './data.json';
import Alpine from 'alpinejs'

window.Alpine = Alpine

const showElement = (elem, chamber, filter) => {
    filter = filter.toLowerCase()
    const result = elem.report_id.toLowerCase().includes(chamber) &&
        (elem.report_title.toLowerCase().includes(filter) ||
        elem.report_id.toLowerCase().includes(filter) ||
        elem.report_committee.toLowerCase().includes(filter))
    return result;
}

Alpine.store('reports',{
    open: true,
    data: data,
    showElement: showElement
})

Alpine.start()
