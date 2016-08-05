import Ember from 'ember';
import EmberHighcharts from 'ember-highcharts/components/high-charts';
import mapData from '../data/europe';

export default Ember.Controller.extend({
 	mode: 'Map',
 	topics: ['Customs', 'Fisheries and Aquaculture', 'Economic and Financial Affairs', 'Public Health', 'Development','Employment and Social Affairs', 'Trade'],
 	data: [],

 	chartOptions: {
 		title: {
 			text: 'Organizations Map'
 		},
 		colorAxis: {
 			min: 0
 		}
 	},

 	chartData: function() {
 		var data = this.get('data');
 		return [{
 			name: 'Issues',
 			data: data, 
 			joinBy: 'hc-key',
 			mapData: mapData,
 			dataLabels: {
	        	enabled: true,
	        	format: '{point.name}'
	      	}
 		}];
 	}.property('data'),

 	actions: {
 		selectTopic: function(topic) {
 			Ember.$.ajax({
 				url: '/search_issues/'+topic,
 				type: 'GET',
 				contentType: 'application/json',
 			}).then((response) => {
 				this.set('data', response);
 			});
 		}
 	}
});