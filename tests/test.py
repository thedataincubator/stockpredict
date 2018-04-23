import unittest
import requests
import responses
import simplejson as json
from stockticker import create_app, query_quandl, QuandlException

QUANDL_URL = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json'
QUANDL_DATA = json.loads("""{
   "datatable":{
      "data":[
         [
            "GOOGL",
            "2018-03-01",
            1109.54,
            1111.27,
            1067.29,
            1071.41,
            2766856.0,
            0.0,
            1.0,
            1109.54,
            1111.27,
            1067.29,
            1071.41,
            2766856.0
         ],
         [
            "GOOGL",
            "2018-03-02",
            1057.98,
            1086.89,
            1050.11,
            1084.14,
            2508145.0,
            0.0,
            1.0,
            1057.98,
            1086.89,
            1050.11,
            1084.14,
            2508145.0
         ],
         [
            "GOOGL",
            "2018-03-05",
            1078.13,
            1101.18,
            1072.27,
            1094.76,
            1432369.0,
            0.0,
            1.0,
            1078.13,
            1101.18,
            1072.27,
            1094.76,
            1432369.0
         ],
         [
            "GOOGL",
            "2018-03-06",
            1102.1,
            1105.63,
            1094.5,
            1100.9,
            1169068.0,
            0.0,
            1.0,
            1102.1,
            1105.63,
            1094.5,
            1100.9,
            1169068.0
         ],
         [
            "GOOGL",
            "2018-03-07",
            1092.82,
            1116.2,
            1089.91,
            1115.04,
            1537429.0,
            0.0,
            1.0,
            1092.82,
            1116.2,
            1089.91,
            1115.04,
            1537429.0
         ],
         [
            "GOOGL",
            "2018-03-08",
            1117.2,
            1131.44,
            1117.2,
            1129.38,
            1510478.0,
            0.0,
            1.0,
            1117.2,
            1131.44,
            1117.2,
            1129.38,
            1510478.0
         ],
         [
            "GOOGL",
            "2018-03-09",
            1139.5,
            1161.0,
            1134.29,
            1160.84,
            2070174.0,
            0.0,
            1.0,
            1139.5,
            1161.0,
            1134.29,
            1160.84,
            2070174.0
         ],
         [
            "GOOGL",
            "2018-03-12",
            1165.05,
            1178.16,
            1159.2,
            1165.93,
            2129297.0,
            0.0,
            1.0,
            1165.05,
            1178.16,
            1159.2,
            1165.93,
            2129297.0
         ],
         [
            "GOOGL",
            "2018-03-13",
            1171.83,
            1178.0,
            1134.57,
            1139.91,
            2129435.0,
            0.0,
            1.0,
            1171.83,
            1178.0,
            1134.57,
            1139.91,
            2129435.0
         ],
         [
            "GOOGL",
            "2018-03-14",
            1145.8,
            1159.76,
            1142.35,
            1148.89,
            2033697.0,
            0.0,
            1.0,
            1145.8,
            1159.76,
            1142.35,
            1148.89,
            2033697.0
         ],
         [
            "GOOGL",
            "2018-03-15",
            1149.57,
            1162.5,
            1135.66,
            1150.61,
            1623868.0,
            0.0,
            1.0,
            1149.57,
            1162.5,
            1135.66,
            1150.61,
            1623868.0
         ],
         [
            "GOOGL",
            "2018-03-16",
            1155.35,
            1156.81,
            1131.36,
            1134.42,
            2654602.0,
            0.0,
            1.0,
            1155.35,
            1156.81,
            1131.36,
            1134.42,
            2654602.0
         ],
         [
            "GOOGL",
            "2018-03-19",
            1117.76,
            1119.37,
            1088.92,
            1100.07,
            3076349.0,
            0.0,
            1.0,
            1117.76,
            1119.37,
            1088.92,
            1100.07,
            3076349.0
         ],
         [
            "GOOGL",
            "2018-03-20",
            1098.4,
            1105.55,
            1082.42,
            1095.8,
            2709310.0,
            0.0,
            1.0,
            1098.4,
            1105.55,
            1082.42,
            1095.8,
            2709310.0
         ],
         [
            "GOOGL",
            "2018-03-21",
            1092.57,
            1108.7,
            1087.21,
            1094.0,
            1990515.0,
            0.0,
            1.0,
            1092.57,
            1108.7,
            1087.21,
            1094.0,
            1990515.0
         ],
         [
            "GOOGL",
            "2018-03-22",
            1080.01,
            1083.92,
            1049.64,
            1053.15,
            3418154.0,
            0.0,
            1.0,
            1080.01,
            1083.92,
            1049.64,
            1053.15,
            3418154.0
         ],
         [
            "GOOGL",
            "2018-03-23",
            1051.37,
            1066.78,
            1024.87,
            1026.55,
            2413517.0,
            0.0,
            1.0,
            1051.37,
            1066.78,
            1024.87,
            1026.55,
            2413517.0
         ],
         [
            "GOOGL",
            "2018-03-26",
            1050.6,
            1059.27,
            1010.58,
            1054.09,
            3272409.0,
            0.0,
            1.0,
            1050.6,
            1059.27,
            1010.58,
            1054.09,
            3272409.0
         ],
         [
            "GOOGL",
            "2018-03-27",
            1063.9,
            1064.54,
            997.62,
            1006.94,
            2940957.0,
            0.0,
            1.0,
            1063.9,
            1064.54,
            997.62,
            1006.94,
            2940957.0
         ]
      ],
      "columns":[
         {
            "name":"ticker",
            "type":"String"
         },
         {
            "name":"date",
            "type":"Date"
         },
         {
            "name":"open",
            "type":"BigDecimal(34,12)"
         },
         {
            "name":"high",
            "type":"BigDecimal(34,12)"
         },
         {
            "name":"low",
            "type":"BigDecimal(34,12)"
         },
         {
            "name":"close",
            "type":"BigDecimal(34,12)"
         },
         {
            "name":"volume",
            "type":"BigDecimal(37,15)"
         },
         {
            "name":"ex-dividend",
            "type":"BigDecimal(42,20)"
         },
         {
            "name":"split_ratio",
            "type":"double"
         },
         {
            "name":"adj_open",
            "type":"BigDecimal(50,28)"
         },
         {
            "name":"adj_high",
            "type":"BigDecimal(50,28)"
         },
         {
            "name":"adj_low",
            "type":"BigDecimal(50,28)"
         },
         {
            "name":"adj_close",
            "type":"BigDecimal(50,28)"
         },
         {
            "name":"adj_volume",
            "type":"double"
         }
      ]
   },
   "meta":{
      "next_cursor_id":null
   }
}""")



class TestApp(unittest.TestCase):

    def setUp(self):
        self.url = 'http://a_url'
        self.secret_key = 'a'
        self.quandl_key = 'b'
        app = create_app(self.url, self.secret_key, self.quandl_key, 7)
        app.testing = True
        self.app = app.test_client()

    @responses.activate
    def test_post_error(self):
        """If our POST request to Prophet errors out, our web app will still
        return a page"""
        responses.add(responses.GET, QUANDL_URL, json=QUANDL_DATA, status=200)
        responses.add(responses.POST, self.url,
                      json={'error': 'not found'}, 
                      status=404)
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)

    @responses.activate
    def test_post_success(self):
        responses.add(responses.GET, QUANDL_URL, json=QUANDL_DATA, status=200)
        responses.add(responses.POST, self.url,
                      json={'ds': [1,2,3,4],
                            'yhat': [2,3,4,5]},
                      status=200)
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)

    @responses.activate
    def test_quandl_success(self):
        responses.add(responses.GET, QUANDL_URL, json=QUANDL_DATA, status=200)
        df = query_quandl('', '', 'open')
        self.assertEqual(list(df.columns), ['ds', 'y'])
        self.assertEqual(len(QUANDL_DATA['datatable']['data']),
                         df.shape[0])
        for ind, col in zip([1, 2], ['ds', 'y']):
            data = map(lambda x : x[ind], 
                    QUANDL_DATA['datatable']['data'])

            self.assertTrue((data == df[col].values).all())

    @responses.activate
    def _test_quandl_error(self, status):
        responses.add(responses.GET, QUANDL_URL, json={}, status=status)
        with self.assertRaises(QuandlException) as e:
            query_quandl('', '')

    def test_quandl_fail(self):
        self._test_quandl_error(404)
        self._test_quandl_error(503)
        
