# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


def generate():
    load_dotenv()
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""
{open("prompt_content.txt", "r").read()}
An incandescent light bulb, incandescent lamp or incandescent light globe is an electric light with a
wire filament that is heated until it glows. The filament is enclosed in a glass bulb that is either
evacuated or filled with inert gas to protect the filament from oxidation. Current is supplied to the
filament by terminals or wires embedded in the glass. A bulb socket provides mechanical support
and electrical connections.
Incandescent bulbs are manufactured in a wide range of sizes, light output, and voltage ratings,
from 1.5 volts to about 300 volts. They require no external regulating equipment, have low
manufacturing costs, and work equally well on either alternating current or direct current. As a
result, the incandescent bulb became widely used in household and commercial lighting, for
portable lighting such as table lamps, car headlamps, and flashlights, and for decorative and
advertising lighting.
Incandescent bulbs are much less efficient than other types of electric lighting. Less than 5% of the
energy they consume is converted into visible light; the rest is lost as heat. The luminous efficacy of
a typical incandescent bulb for 120 V operation is 16 lumens per watt (lm/W), compared with 60
lm/W for a compact fluorescent bulb or 100 lm/W for typical white LED lamps.
The heat produced by filaments is used in some applications, such as heat lamps in incubators, lava
lamps, and the Easy-Bake Oven toy. Quartz envelope halogen infrared heaters are used for
industrial processes such as paint curing and space heating.
Incandescent bulbs typically have short lifetimes compared with other types of lighting; around
1,000 hours for home light bulbs versus typically 10,000 hours for compact fluorescents and 20,000–
30,000 hours for lighting LEDs. Most incandescent bulbs can be replaced by fluorescent lamps,
high-intensity discharge lamps, and light-emitting diode lamps (LED). Some governments have
begun a phase-out of incandescent light bulbs to reduce energy consumption.
History
Historians Robert Friedel and Paul Israel list inventors of incandescent lamps prior to Joseph Swan
and Thomas Edison of General Electric. They conclude[citation needed] that Edison's version was
able to outstrip the others because of a combination of three factors: an effective incandescent
material, a higher vacuum than others were able to achieve (by use of the Sprengel pump) and a
high resistance that made power distribution from a centralized source economically viable.
Historian Thomas Hughes has attributed Edison's success to his development of an entire,
integrated system of electric lighting.
The lamp was a small component in his system of electric lighting, and no more critical to its
effective functioning than the Edison Jumbo generator, the Edison main and feeder, and the
parallel-distribution system. Other inventors with generators and incandescent lamps, and with
comparable ingenuity and excellence, have long been forgotten because their creators did not
preside over their introduction in a system of lighting.
Early pre-commercial research
In 1761, Ebenezer Kinnersley demonstrated heating a wire to incandescence.
In 1802, Humphry Davy used what he described as "a battery of immense size", consisting of 2,000
cells housed in the basement of the Royal Institution of Great Britain, to create an incandescent
light by passing the current through a thin strip of platinum, chosen because the metal had an
extremely high melting point. It was not bright enough nor did it last long enough to be practical,
but it was the precedent behind the efforts of scores of experimenters over the next 75 years.
Over the first three-quarters of the 19th century, many experimenters worked with various
combinations of platinum or iridium wires, carbon rods, and evacuated or semi-evacuated
enclosures. Many of these devices were demonstrated and some were patented.
In 1835, James Bowman Lindsay demonstrated a constant electric light at a public meeting in
Dundee, Scotland. He stated that he could "read a book at a distance of one and a half feet".
However he did not develop the electric light any further.
In 1838, Belgian lithographer Marcellin Jobard invented an incandescent light bulb with a vacuum
atmosphere using a carbon filament.
In 1840, British scientist Warren De la Rue enclosed a coiled platinum filament in a vacuum tube
and passed an electric current through it. The design was based on the concept that the high
melting point of platinum would allow it to operate at high temperatures and that the evacuated
chamber would contain fewer gas molecules to react with the platinum, improving its longevity.
Although a workable design, the cost of the platinum made it impractical for commercial use. In
1841, Frederick de Moleyns of England was granted the first patent for an incandescent lamp, with
a design using platinum wires contained within a vacuum bulb. He also used carbon.
In 1845, American John W. Starr patented an incandescent light bulb using carbon filaments. His
invention was never produced commercially. In 1851, Jean Eugène Robert-Houdin publicly
demonstrated incandescent light bulbs on his estate in Blois, France. His light bulbs are on display
in the museum of the Château de Blois. In 1859, Moses G. Farmer built an electric incandescent light
bulb using a platinum filament. Thomas Edison later saw one of these bulbs in a shop in Boston,
and asked Farmer for advice on the electric light business.
In 1872, Russian Alexander Lodygin invented an incandescent light bulb and obtained a Russian
patent in 1874. He used as a burner two carbon rods of diminished section in a glass receiver,
hermetically sealed, and filled with nitrogen, electrically arranged so that the current could be
passed to the second carbon when the first had been consumed. Later he lived in the US, changed
his name to Alexander de Lodyguine and applied for and obtained patents for incandescent lamps
having chromium, iridium, rhodium, ruthenium, osmium, molybdenum and tungsten filaments,
and a bulb using a molybdenum filament was demonstrated at the world fair of 1900 in Paris.
On 24 July 1874, a Canadian patent was filed by Henry Woodward and Mathew Evans for a lamp
consisting of carbon rods mounted in a nitrogen-filled glass cylinder. They were unsuccessful at
commercializing their lamp, and sold rights to their patent (U.S. Patent 181,613) to Thomas Edison
in 1879. (Edison needed ownership of the novel claim of lamps connected in a parallel circuit).
On 4 March 1880, just five months after Edison's light bulb, Alessandro Cruto created his first
incandescent lamp. Cruto produced a filament by deposition of graphite on thin platinum
filaments, by heating it with an electric current in the presence of gaseous ethyl alcohol. Heating
this platinum at high temperatures leaves behind thin filaments of platinum coated with pure
graphite. By September 1881 he had achieved a successful version of the first synthetic filament.
The light bulb invented by Cruto lasted five hundred hours as opposed to the forty of Edison's
original version. In 1882 Munich Electrical Exhibition in Bavaria, Germany Cruto's lamp was more
efficient than the Edison's one and produced a better, white light.[26]
In 1893, Heinrich Göbel claimed he had designed the first incandescent light bulb in 1854, with a
thin carbonized bamboo filament of high resistance, platinum lead-in wires in an all-glass
envelope, and a high vacuum. Judges of four courts raised doubts about the alleged Göbel
anticipation, but there was never a decision in a final hearing due to the expiration of Edison's
patent. A research work published in 2007 concluded that the story of the Göbel lamps in the 1850s
is fictitious.
Commercialization
Joseph Swan (1828–1914) was a British physicist and chemist. In 1850, he began working with
carbonized paper filaments in an evacuated glass bulb. By 1860, he was able to demonstrate a
working device but the lack of a good vacuum and an adequate supply of electricity resulted in a 
short lifetime for the bulb and an inefficient source of light. By the mid-1870s better pumps had
become available, and Swan returned to his experiments.
With the help of Charles Stearn, an expert on vacuum pumps, in 1878, Swan developed a method of
processing that avoided the early bulb blackening. This received a British Patent in 1880. On 18
December 1878, a lamp using a slender carbon rod was shown at a meeting of the Newcastle
Chemical Society, and Swan gave a working demonstration at their meeting on 17 January 1879. It
was also shown to 700 who attended a meeting of the Literary and Philosophical Society of
Newcastle upon Tyne on 3 February 1879. These lamps used a carbon rod from an arc lamp rather
than a slender filament. Thus they had low resistance and required very large conductors to supply
the necessary current, so they were not commercially practical, although they did furnish a
demonstration of the possibilities of incandescent lighting with relatively high vacuum, a carbon
conductor, and platinum lead-in wires. This bulb lasted about 40 hours.
Swan then turned his attention to producing a better carbon filament and the means of attaching
its ends. He devised a method of treating cotton to produce 'parchmentised thread' in the early
1880s and obtained British Patent 4933 that same year. From this year he began installing light
bulbs in homes and landmarks in England. His house, Underhill, Low Fell, Gateshead, was the first
in the world to be lit by a lightbulb. In the early 1880s he had started his company. In 1881, the
Savoy Theatre in the City of Westminster, London was lit by Swan incandescent lightbulbs, which
was the first theatre, and the first public building in the world, to be lit entirely by electricity. The
first street in the world to be lit by an incandescent lightbulb was Mosley Street, Newcastle upon
Tyne, United Kingdom. It was lit by Joseph Swan's incandescent lamp on 3 February 1879.
Thomas Edison began serious research into developing a practical incandescent lamp in 1878.
Edison filed his first patent application for "Improvement in Electric Lights" on 14 October 1878.
After many experiments, first with carbon in the early 1880s and then with platinum and other
metals, in the end Edison returned to a carbon filament.[36] The first successful test was on 22
October 1879, and lasted 13.5 hours. Edison continued to improve this design and by 4 November
1879, filed for a US patent for an electric lamp using "a carbon filament or strip coiled and
connected ... to platina contact wires." Although the patent described several ways of creating the
carbon filament including using "cotton and linen thread, wood splints, papers coiled in various
ways," Edison and his team later discovered that a carbonized bamboo filament could last more
than 1200 hours. In 1880, the Oregon Railroad and Navigation Company steamer, Columbia, became
the first application for Edison's incandescent electric lamps (it was also the first ship to use a
dynamo).
Albon Man, a New York lawyer, started Electro-Dynamic Light Company in 1878 to exploit his
patents and those of William Sawyer.Weeks later the United States Electric Lighting Company was
organized. This company did not make their first commercial installation of incandescent lamps
until the fall of 1880, at the Mercantile Safe Deposit Company in New York City, about six months
after the Edison incandescent lamps had been installed on the Columbia. Hiram S. Maxim was the
chief engineer at the United States Electric Lighting Company. After the great success in the United
States, the incandescent light bulb patented by Edison also began to gain widespread popularity in
Europe as well; among other places, the first Edison light bulbs in the Nordic countries were
installed at the weaving hall of the Finlayson's textile factory in Tampere, Finland in March 1882.
Lewis Latimer, employed at the time by Edison, developed an improved method of heat-treating
carbon filaments which reduced breakage and allowed them to be molded into novel shapes, such
as the characteristic "M" shape of Maxim filaments. On 17 January 1882, Latimer received a patent
for the "Process of Manufacturing Carbons", an improved method for the production of light bulb
filaments, which was purchased by the United States Electric Light Company. Latimer patented
other improvements such as a better way of attaching filaments to their wire supports.
In Britain, the Edison and Swan companies merged into the Edison and Swan United Electric
Company (later known as Ediswan, and ultimately incorporated into Thorn Lighting Ltd). Edison
was initially against this combination, but Edison was eventually forced to cooperate and the
merger was made. Eventually, Edison acquired all of Swan's interest in the company. Swan sold his
US patent rights to the Brush Electric Company in June 1882.
The United States Patent Office gave a ruling 8 October 1883, that Edison's patents were based on
the prior art of William Sawyer and were invalid. Litigation continued for a number of years.
Eventually on 6 October 1889, a judge ruled that Edison's electric light improvement claim for "a
filament of carbon of high resistance" was valid
"""),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
        tools=tools,
        system_instruction=[
            types.Part.from_text(text=f"{open("prompt_text.txt", "r").read()}\n{open("prompt_content.txt", "r").read()}"),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
