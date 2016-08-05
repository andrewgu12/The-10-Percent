import Ember from 'ember';
import mapData from '../data/europe';

export default Ember.Controller.extend({
 	chartOptions: {
 		title: {
 			text: 'Average Sentiment By Country'
 		},
 		colorAxis: {
 			min: 0
 		},
 		mapNavigation: {
            enabled: true,
            buttonOptions: {
                verticalAlign: 'bottom'
            }
        }
 	},
 	mode: 'Map',
 	data: [],

 	chartData: function() {
 		var data = this.get('data');
 		console.log(this.get('data'));
 		return [{
 			name: 'Issues',
 			data: data, 
 			joinBy: 'hc-key',
 			mapData: mapData,
 			dataLabels: {
	        	enabled: true,
	        	format: '{point.name}'
	      	},
	      	states: {
                hover: {
                    color: '#BADA55'
                }
            }
	    }];
 	}.property('data'),


 	actions: {
 		getData: function() {
 			Ember.$.ajax({
	 			url: '/comments/52016PC0482',
	 			contentType: 'application/json',
	 			type: 'GET'
	 		}).then((response) => {
	 			this.set('data', response);
	 		});
	 	}
 	}
});