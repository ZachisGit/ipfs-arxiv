var page_index = 1;
var page_count = 0;
var entries_per_page = 20;

window.onload = function()
{
	var url_string = window.location.href;
	var url = new URL(url_string);
	page_index = url.searchParams.get('page');

	if (page_index == null || isNaN(parseInt(page_index)) || parseInt(page_index) == "")
		page_index = 1;
	else
		page_index = parseInt(page_index);

	page_count = Math.ceil((index_json.length)/entries_per_page);

	if (page_index > page_count)
		page_index = 1;

	display_available_pages();
	display_entries();
}

function display_available_pages()
{
	var page_idx = document.getElementById('page_idx'); 
	page_idx.innerHTML = page_index;
	var page_total = document.getElementById('page_total'); 
	page_total.innerHTML = page_count;

}

function display_entries()
{
	var page_start = page_index;
	var page_length = entries_per_page;

	if (page_index+page_length > index_json.length)
		page_length = index_json.length-((page_count-1)*entries_per_page);

	for (var i = page_start-1; i < page_start+page_length-1; i++)
	{
		var entry = get_entry_tag(index_json[i]);
		document.getElementById('main').appendChild(entry);
	}
	document.getElementById('main').removeChild(document.getElementById('base_entry'));
}

function get_entry_tag(json_entry)
{
	var tobecloned = document.getElementById('base_entry');
	var clone = tobecloned.cloneNode(true);

	clone.id = '';
	clone.getElementsByClassName('entry_title')[0].innerHTML = json_entry['title'];
	clone.getElementsByClassName('entry_summary')[0].innerHTML = json_entry['summary'];
	clone.getElementsByClassName('entry_id')[0].innerHTML = json_entry['id'];
	clone.getElementsByClassName('entry_download')[0].href = 'pdfs/'+json_entry['id']+'.pdf';
	return clone;
}

function next_page()
{
	if (page_index + 1 > page_count)
		page_index = 1;
	else
		page_index++;
	window.location.href = "index.html?page="+page_index;
}

function prev_page()
{
	if (page_index - 1 <= 0)
		page_index = page_count;
	else
		page_index--;
	window.location.href = "index.html?page="+page_index;
}