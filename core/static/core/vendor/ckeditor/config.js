CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	config.filebrowserBrowseUrl = '/vendor/kcfinder/browse.php?opener=ckeditor&type=files';
	config.filebrowserImageBrowseUrl = '/vendor/kcfinder/browse.php?opener=ckeditor&type=images';
	config.filebrowserFlashBrowseUrl = '/vendor/kcfinder/browse.php?opener=ckeditor&type=flash';
	config.filebrowserUploadUrl = '/vendor/kcfinder/upload.php?opener=ckeditor&type=files';
	config.filebrowserImageUploadUrl = '/vendor/kcfinder/upload.php?opener=ckeditor&type=images';
	config.filebrowserFlashUploadUrl = '/vendor/kcfinder/upload.php?opener=ckeditor&type=flash';
	//do not add extra paragraph to html
	config.autoParagraph = false;
};
