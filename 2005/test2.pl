  use SOAP::Lite;
  print SOAP::Lite
    -> service('http://www.xmethods.net/sd/StockQuoteService.wsdl')
    -> getQuote('MSFT'), "\n";