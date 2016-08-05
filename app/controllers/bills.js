import Ember from 'ember';

export default Ember.Controller.extend({
	billData: null,
	value: '',
	similarUSBills: [],
	similarEUBills: [],
	keyPhrases: [],

	actions: {
		getBills: function() {
			var value = this.get('value');

			Ember.$.ajax({
				url: '/search_bills/'+value,
				type: 'GET',
				contentType: 'application/json',
			}).then((response) => {
				console.log(response);
				this.set('billData', response.bills);
			});
		},

		getSimilarBills: function(id) {
			Ember.$.ajax({
				url: '/bill_info/'+id,
				type: 'GET',
				contentType: 'application/json',
			}).then((response) => {
				this.set('similarUSBills', response.us_bills);
				this.set('similarEUBills', response.eu_bills);
				this.set('keyPhrases', response.phrases);
				console.log(response.phrases);
				Ember.$('#similarBillsModal').modal('show');
			});
		},

		closeModal: function() {
			console.log('exit modal');
			this.setProperties({
				similarEUBills: [],
				similarUSBills: [],
				keyPhrases: []
			});
		}
	}
});