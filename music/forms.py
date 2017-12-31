from django import forms

class SearchForm(forms.Form):
	item = forms.CharField(
		required = True,
		label = 'Item',
		max_length = 100
		)

class ReviewForm(forms.Form):
	review = forms.CharField(
		widget = forms.Textarea,
		required = True,
		label = 'Review',
		)