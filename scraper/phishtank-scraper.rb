require 'phishtank_scraper'
require 'json'


pt_scraper = PhishtankScraper.new
submissions = pt_scraper.page_scrape((0..1), {active: "y", valid: "y"})
submissions_json = submissions.to_json
#puts (submissions_json)
begin
  file = File.open("links.json", "w")
  file.write(submissions_json)
rescue IOError => e
  #some error occur, dir not writable etc.
ensure
  file.close unless file.nil?
end
