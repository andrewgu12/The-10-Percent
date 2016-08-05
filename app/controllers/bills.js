import Ember from 'ember';

export default Ember.Controller.extend({
	billData: null,
	value: '',

	actions: {
		getBills: function() {
			console.log(this.get('value'));
			this.set('billData', []);
		}
	}
});