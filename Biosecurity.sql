use Biosecurity;

CREATE TABLE IF NOT EXISTS forester
(
forester_id INT auto_increment PRIMARY KEY NOT NULL,
roles varchar(10) not null default "forester", 
first_name varchar(30) not null,
family_name varchar(30) not null,
status_now tinyint not null default 1,
address varchar(500),
email varchar(300) not null,
phone varchar(11) not null,
date_joined date,
pin varchar(200) not null
);


CREATE TABLE IF NOT EXISTS staff_admin
(
staff_id INT auto_increment PRIMARY KEY NOT NULL,
roles varchar(10) default "staff",
first_name varchar(30) not null,
family_name varchar(30) not null,
status_now tinyint default 1,
email varchar(300) not null,
phone varchar(11) not null,
hire_date date,
staff_position varchar(100),
department varchar(100),
pin varchar(200) not null
);


CREATE TABLE IF NOT EXISTS users
(
roles varchar(10),
forester_id INT,
staff_id INT,
pin varchar(200),
status_now tinyint,
FOREIGN KEY (forester_id) REFERENCES forester(forester_id)
ON UPDATE CASCADE
ON DELETE CASCADE,
FOREIGN KEY (staff_id) REFERENCES staff_admin(staff_id)
ON UPDATE CASCADE
ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS forestry
(
forestry_id INT auto_increment PRIMARY KEY NOT NULL,
forestry_type  varchar(7) not null,
present_in_nz tinyint not null,
common_name varchar(100) not null,
scientific_name varchar(100) not null,
key_charac text,
biology text,
symptoms text,
image_num int
);


CREATE TABLE IF NOT EXISTS images
(
image_num INT auto_increment PRIMARY KEY NOT NULL,
forestry_id INT NOT NULL,
images text,
show_p tinyint default 0,
FOREIGN KEY (forestry_id) REFERENCES forestry(forestry_id)
on update cascade
ON DELETE CASCADE
);


INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (1, 'pest', 1, 'Fir adelgid', 'Adelges nordmannianae', 'The usual form of the fir adelgid in New Zealand is wingless. Sapsucking activity by the fir adelgid can cause loss of vigour in and sometimes death of a tree.', 'The adult is approximately 1 mm long, rounded in shape, and strongly convex. It is purplish-brown, with the head and thorax being slightly darker than the abdomen. Only by using a microscope can the six legs, minute antennae, and fine hair-like mouthparts be seen. On the upper surface of the head, thorax, and abdomen there are groups of glands which produce the waxy-like filaments which cover the insect.', 'Insertion of the insect’s stylet mouthparts into the plant tissues provokes abnormal cell growth, which in turn blocks normal water conduction and causes trees heavily attacked over several years to suffer severe loss of foliage or produce stunted, often discoloured, shoots and needles.');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (2, 'pest', 1, 'Puriri moth', 'Aenetus virescens', 'The moth is the largest in New Zealand, with a wingspan up to 150 mm in the female and 100 mm in the male.', 'The moths are usually green, but the intensity of colour and wing patterning is very variable (Fig. 3). Miller (1971), who describes the moth and its life history, records the occurrence of bright-yellow, brick-red, almost scarlet, and even albino specimens. The females have a dark-brown or black mottled pattern on the forewings and the hind wings are usually buff coloured. The markings of the male\'s forewings are white and the hind wings are greener than those of the female.', 'Although caterpillars are usually found in relatively small-diameter stems and branches (up to 30 cm), the tunnel system persists indefinitely after the adult has emerged. The entrance hole is eventually occluded by callus tissue and further growth, but the old tunnel serves as a focus for core rots.');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (3, 'pest', 1, 'Two-toothed longhorn', 'Ambeodontus tristis', 'Adults emerge in autumn or early winter and tend to avoid light.', 'The adult female is red-brown to black and up to 25 mm long, although the size is variable possibly depending on nutrition, temperature, and wood moisture. The head projects forward and, at rest, the thread-like antennae extend about halfway down the body. The prothorax, which is narrowest where it joins the elytra (wing cases), has two shiny raised areas on the top and a prominence on each side. These prominences give the beetle its common name, \"two-toothed\". The elytra are parallel-sided and densely covered in short, pale yellow hairs which become worn away in older specimens. The male is similar in appearance to the female but possesses longer antennae extending about three-quarters down the body.', 'The larvae of the two-toothed longhorn beetle bore in dead softwoods. They may be found in both the sapwood and the heartwood of timbers in use, logs, branches, and dead trees. Successful infestation also occurs in living trees where access to the heartwood can be gained through logging wounds and dead branch stubs. The early larval tunnels run predominantly with the grain but later tunnels run in all directions. Severe infestations may reduce timber to a thin outer shell. ');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (4, 'pest', 1, 'Large cicadas', 'Amphipsalta spp.', 'Amphipsalta are mottled green and black, and can be recognised from other cicadas by their large size (body length greater than 19 mm). ', 'In New Zealand there are about 30 species of cicada and all are similar in shape. The adults are stout with two pairs of large, distinctly veined, transparent wings folded tent-like over the abdomen when at rest. The front edge of the forewing is strongly veined. The head is broad with prominent compound eyes and short bristle-like antennae. Three simple eyes are arranged in a triangle on top of the head. Long piercing tube-like mouthparts extend beneath the thorax. The abdomen tapers to the rear, and the female has a short spear-like ovipositor underneath near the tip.', 'The major damage is caused by the female piercing plant tissues with her ovipositor to lay eggs. The cuts made by the three species of Amphipsalta form a herringbone pattern , and twigs and branches so affected may be sufficiently weakened to break in high winds. Such broken branches on conifers show up as reddish \"flags\" in the canopy when the foliage dies. Open cuts also provide entry for pathogens and wood-boring insects. Often the cuts heal over making the twigs gnarled in appearance.\n');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (5, 'pest', 1, 'Black pine bark beetle', 'Hylastes ater', 'The head is directed downwards and is prolonged into a short snout. The pronotum appears shining.', 'The beetles are about 4-5 mm long and 1.4 mm wide, approximately cylindrical in shape, with sides nearly parallel. They are black except for the antennae and the terminal segments of the legs, which are reddish brown. Newly developed adults are uniformly reddish brown, and in young adults the elytra (wing cases) may retain this colour after other parts have darkened.', 'Brood galleries are made mostly in the roots of stumps and dead trees but also occur at the bases of dead trees and in logs in contact with the ground. Neither adult nor larval tunnels engrave the sapwood except in small diameter material. Reddish frass is expelled from adult tunnels and is found throughout workings in the inner bark.');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (6, 'disease', 1, 'Root disease', 'Armillaria', 'Young pines (up to ca. 7-years-old): foliage changes from deep green, through pale green, yellow, and finally brick red-to-brown. Dead needles remain firmly attached for some time. Older pines: Crowns on infected trees remain deep green and healthy (non-lethal or chronic infection, detected only by examination of the stem base below soil level).', 'The fungi infect the root system and lower stem of the tree host. Mortality of young trees may occur or growth may be reduced.', 'They cause a characteristic heart rot in living native trees, and are also widespread in coarse woody debris. Wood decayed by these fungi is wet, yellowish, and divided into large pockets by black lines.');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (7, 'disease', 1, 'Needle cast', 'Cyclaneusma', 'Affected trees are scattered among unaffected trees – disease is not uniform in a stand unless the trees are genetically identical.', 'In spring (late August/September), foliage over all or part of a tree crown turns a mottled yellow-green, then brown. Most infected needles prematurely shed by December.', 'Needles turn mottled yellow and then brown\nNeedles often have transverse bands develop during the later stages of disease development\nNeedles remain rigid, and are very easily removed from branch\nThe entire tree crown may be affected\nSymptoms start September or October, with a second (usually less severe) cast occurring around April\nAfter the needles are cast the tree crown appears very thin\nTrees aged between about 6 and 20 years are affected');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (8, 'disease', 1, 'Nursery disease', 'Colletotrichum acutatum', 'Crook-shaped stem terminal which may become reddish. Terminals of developing laterals may also be deformed.', 'The terminal region of the stem of young seedlings grows around through 180 degrees, and its continued growth is suppressed.', 'Some dead needles on the malformed terminal. In severe cases, all needles in this region die and the stem becomes necrotic. Pink, pustule-like fruiting bodies of the fungus may be visible on dead needles.\nStem becomes stiff with abnormal increase in diameter growth.\nDiseased seedlings shorter than uninfected seedlings.');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (9, 'disease', 1, 'Acacia rust', 'Uromycladium spp.', 'Leaf spots, and branch and stem distortions.', 'Large galls on branches and stems cause dieback, and sometimes tree death.', 'Large, convoluted, brown galls on branches, stems, and seed pods.\nSmaller blister-like galls on leaves and petioles.\nDieback of branches beyond the galls.\nDeath of young trees.');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (10, 'disease', 1, 'Myrtle rust', 'Austropuccinia psidii', 'Rust fungi disperse readily by airborne urediniospores.', 'Myrtle rust, caused by the microscopic fungus Puccinia psidii, has been discussed in earlier issues of Forest Health News (211, 212, 238 and 255). Although native to tropical South America, it has dispersed globally on plants in the family Myrtaceae. One strain has reached a number of Asian and Pacific countries during the past decade and is now sitting on New Zealand’s doorstep. The NZ Forest Owners Association have asked the Forest Protection Group (Scion) to examine what an introduction of this disease might mean for forestry.', 'Bright yellow powdery eruptions appearing on the underside of the leaf in a young infection\nBright yellow powdery eruptions on both sides of the leaf in a mature infection\nBrown or grey rust pustules − older spores − on older lesions.');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (11, 'pest', 0, 'Spongy moth', 'Lymantria dispar', 'The official new common name is the spongy moth, in reference to the physical appearance of its egg batches', 'Lymantria dispar, commonly known as the gypsy moth (Figure 1) is one of the most destructive pests of shade, fruit, and ornamental trees throughout the northern hemisphere, and has been nominated as among the world’s worst invasive alien species by the Invasive Species Specialist Group (Global Invasive Species Database, 2011).', 'Lymantria dispar, is a severe defoliator of trees and is described as both an economic and environmental high-impact pest. ');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (12, 'pest', 0, 'Poplar sawfly', 'Cladius grandis', 'The adult flies are 6-9mm in length, mostly reddish-yellow and have a black head and a partly black thorax.', 'The adults are about the size of a honey bee, with an orange abdomen and a black head and thorax. Emerging from the soil in October and November to mate, the females are present throughout the summer. They lay their eggs in a neat row down both sides of the petiole, the leaf stalk, of a fully expanded leaf.\n\nEach egg is placed into a little pocket, formed by the action of the saw-like ovipositor. The eggs then take four weeks to hatch, and the tiny pale larvae are first seen in early December. They generally feed side by side, skeletonising the surface of the leaves to leave translucent ‘window’ appearance. As the larvae feed and develop through their six instars, any time between December and March, they grow in size and become a brighter yellow with distinctive black dots. When they reach their fourth instar the larvae are big enough to chew through the entire leaf, as seen in the photographs.', 'The hairy poplar sawfly is currently only a minor pest, removing up to a fifth of the leaf area from the lower branches of young poplars. ');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (13, 'pest', 0, 'Sycamore lace bug', 'Corythucha ciliata', 'Although delicate, the adults are very mobile and aided by wind are capable\nof flying many kilometres.', 'All life stages of the bugs occur together on the undersides of the leaves.', 'The upper surface of infested foliage becomes marked with yellowish chlorotic spots and later with brown necrotic spots. The underside of infested leaves becomes marked with black varnish-like excrement spots, and cast skins of previous developmental stages often remain attached to infested leaves. In cases of severe infestation trees may be defoliated in late summer and damage is far more severe during dry weather. These heavy infestations are more common in urban areas than natural settings.');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (14, 'pest', 0, 'European house borer', 'Hylotrupes bajulus', 'EHB is a pest of seasoned softwood timber exotic to Australia.', 'EHB is mainly found in dead pine trees, logs or dead parts of live pine trees in Western Australia. There are 136 infested sites including nine pine plantations. EHB has not yet been found infesting structural timber that was already in a house prior to EHB appearing in Western Australia. However, the potential for infestation is great since many residential developments are occurring adjacent to infested pine plantations.', 'It specifically attacks seasoned pine, spruce and fir. Its larvae are known to cause significant damage in structural softwood timber in buildings, and can also attack furniture. In this instance, in the Perth suburb of Parkerville, the timber beam was infested prior to installation and originated from a local pine wood dealer.');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (15, 'pest', 0, 'Asian Longhorn beetle', 'Anoplophora glabripennis', 'Adult Beetle - large black beetles with white spots on wing covers; antennae have a white band at the base of each segment. ', 'The larvae of the Asian longhorn beetle are wood borers that attack a wide variety of hardwood trees. Their preferred hosts are maples, horse chestnuts, elms, poplars, willows, and birches, and heavy infestation can result in tree death. The Asian longhorn beetle is native to China and Korea where major economic losses occur. Nearly 50% of China\'s extensive poplar plantations have been attacked, and millions of infested forest and urban trees have been felled as a control measure.', 'Normally an infestation is detected only after the appearance of comparatively large emergence holes (> 10 mm diameter), by which time the beetles have already emerged and dispersed to attack new trees. ');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (16, 'disease', 0, 'Western gall rust', 'Peridermium harknessii', 'One of several pine stem rusts, this native of western North America induces rounded galls that deform the branches and stems of trees of a number of 2- and 3-needle pine species. Infected trees become malformed and, when young, suffer breakage and death, all of which could have a serious economic impact on forestry in this country, should the fungus ever become established.', 'Peridermium harknessii (syn. Endocronartium harknessii) has long been viewed as a potential risk to exotic radiata pine plantations in the southern hemisphere because, unlike most rust pathogens, an alternate host is not required to complete the lifecycle. This means that P. harknessii is able to spread directly from pine to pine.', 'The impact of infection can range from volume loss due to branch galls, through to mortality due to stem breakage at a stem gall. Wood quality can also be affected due to characteristic “hip-cankers” on the stem.');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (17, 'disease', 0, 'Pitch canker disease of pines', 'Fusarium circinatum', 'Disease characterised by exudation of copious\namounts of resin.', 'Pitch canker is considered to be endemic in south-eastern United States and has caused damage in plantations of Pinus elliottii and P. taeda in that region. It was first recorded on P. radiata in California in 1986. The disease is now widespread in the Ano Nuevo - Monterey area south of San Francisco and isolated occurrences have been recorded as far south as San Diego. The disease is characterised by copious resin exudation from shoots, branches and stems of infected trees. Needles on infected branches are killed and crown dieback occurs when the disease is well advanced.', 'Naturally occurring and animal/insect caused wounds are required as infection courts for the fungus and researchers in California have found that most, if not all, new infections of P. radiata are insect–vectored. The primary vectors are species of several genera of bark, twig and cone beetles.');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (18, 'disease', 0, 'Needle blight', 'Daño Foliar del Pino', 'From a distance, affected trees appear similar to those affected by Cyclaneusma needle-cast. Foliage turns yellow, gold, and then brown and 1-year-old foliage is affected. However, the resemblance ends there. Needles do not detach from branches as readily as those affected by Cyclaneusma and symptoms often start with a pale area at the base of the needle, accompanied by a black band.', 'DFP is most severe on sites prone to prolonged periods of moisture through low cloud, mist, fog, or rain.', 'In young trees, a number of symptoms are seen. Needles on the underside of branches are\nmore commonly affected than needles on the upper side. The earliest symptom on\nneedles is dark, oily-looking, bands that appear while the needle is still green. These bands\nusually form near the base of the needle rather than near the tip. The bands are translucent\nwhen viewed with a strongly lit background. They become darker over time and\nfinish up black. As disease progresses, affected needles collapse from the base and\nhang down perpendicular to the branch, become yellow, and are cast. They detach readily from\nthe branch. ');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (19, 'pest', 0, 'Pine processionary moth', 'Thaumetopoea pityocampa', '99', 'There are about 300 000 ha of P. radiata in Spain, mainly in the northern Basque region. A few smaller plantations of this species are found in south-west France. These regions also have extensive forests of native pines — P. pinaster, P. nigra, P. sylvestris — in plantations and natural forests.', 'P. radiata were badly damaged, especially younger trees, some having lost all their needles. ');
INSERT INTO `forestry` (`forestry_id`, `forestry_type`, `present_in_nz`, `common_name`, `scientific_name`, `key_charac`, `biology`, `symptoms`) VALUES (20, 'pest', 0, 'Polyphagous shot-hole borer', 'Euwallacea fornicatus', '99', '99', 'This damaging pest infests more than 400 plant species, mostly woody species and carries a few known symbiotic fungi, including the damaging Fusarium euwallaceae. Fusarium euwallaceae infects the vascular tissue of a susceptible tree and can cause dieback and death. The beetle attacks stressed trees primarily but can also attack healthy trees. Plant hosts are divided into two categories: reproductive and non-reproductive. This interaction is dependent on how successful PSHB’s fungal symbiont, symbionts colonise the host\'s tissue. the host’s tissue. In a reproductive host, the fungus will establish well allowing the beetle to thrive, while in a non-reproductive host it will not and the beetle does not complete its lifecycle; however, symptoms may develop.');

INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (1, 1, '1-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (2, 1, '1-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (3, 2, '2-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (4, 2, '2-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (5, 2, '2-3.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (6, 3, '3-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (7, 3, '3-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (8, 4, '4-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (9, 4, '4-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (10, 4, '4-3.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (11, 5, '5-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (12, 5, '5-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (13, 5, '5-3.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (14, 6, '6-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (15, 6, '6-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (16, 6, '6-3.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (17, 7, '7-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (18, 7, '7-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (19, 7, '7-3.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (20, 8, '8-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (21, 8, '8-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (22, 9, '9-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (23, 9, '9-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (24, 9, '9-3.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (25, 9, '9-4.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (26, 10, '10-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (27, 10, '10-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (28, 11, '11-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (29, 11, '11-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (30, 11, '11-3.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (31, 12, '12-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (32, 12, '12-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (33, 12, '12-3.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (34, 12, '12-4.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (35, 13, '13-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (36, 13, '13-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (37, 14, '14-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (38, 14, '14-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (39, 15, '15-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (40, 15, '15-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (41, 16, '16-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (42, 16, '16-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (43, 17, '17-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (44, 17, '17-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (45, 18, '18-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (46, 18, '18-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (47, 18, '18-3.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (48, 19, '19-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (49, 19, '19-2.jpg', 0);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (50, 20, '20-1.jpg', 1);
INSERT INTO `images` (`image_num`, `forestry_id`, `images`, `show_p`) VALUES (51, 20, '20-2.jpg', 0);

INSERT INTO `forester` (`forester_id`, `roles`, `first_name`, `family_name`, `status_now`, `address`, `email`, `phone`, `date_joined`, `pin`) VALUES (1, 'forester', 'David', 'Brown', 1, 'vvv road', 'aaa@gmail.com', '22222222222', '2014-02-27', '4d4a1fce53699e09dd530c2b4805c68427e557c255b14d0e371cc86a524709ad');
INSERT INTO `forester` (`forester_id`, `roles`, `first_name`, `family_name`, `status_now`, `address`, `email`, `phone`, `date_joined`, `pin`) VALUES (2, 'forester', 'Kate', 'Wang', 1, 'bbb road', 'bbb@gmail.com', '11111111112', '2015-02-28', 'a35206016fbc3b8d77e3f2a6fdae3628e1b852a6bc7a1886b50a4a55fb49fd51');
INSERT INTO `forester` (`forester_id`, `roles`, `first_name`, `family_name`, `status_now`, `address`, `email`, `phone`, `date_joined`, `pin`) VALUES (3, 'forester', 'Jane', 'Brown', 1, 'ccc  road', 'ccc@gmail.com', '11111111113', '2016-03-06', '91d2cb6684bd6733a12d286e412d21760796b1d5c2059cd37c51d9fe67a78407');
INSERT INTO `forester` (`forester_id`, `roles`, `first_name`, `family_name`, `status_now`, `address`, `email`, `phone`, `date_joined`, `pin`) VALUES (4, 'forester', 'Roy', 'Lin', 1, 'ddd road', 'ddd@gmail.com', '11111111114', '2017-07-02', 'fcf9415c0f10c6d89fddb6d98fa723483556373f376fec550e71e88cd2d0c4a8');
INSERT INTO `forester` (`forester_id`, `roles`, `first_name`, `family_name`, `status_now`, `address`, `email`, `phone`, `date_joined`, `pin`) VALUES (5, 'forester', 'Olivia', 'Ong', 1, 'eee road', 'eee@gmail.com', '11111111115', '2018-03-03', 'ce47ce71fb20420e7751eba75e721a3035726b99f1253ede644e433dcf33cb4f');
INSERT INTO `forester` (`forester_id`, `roles`, `first_name`, `family_name`, `status_now`, `address`, `email`, `phone`, `date_joined`, `pin`) VALUES (6, 'forester', 'Huizhong', 'Wang', 0, '43 Anaru Road', 'minasopor23@gmail.com', '0204918430', '2024-03-01', '4d4a1fce53699e09dd530c2b4805c68427e557c255b14d0e371cc86a524709ad');
INSERT INTO `forester` (`forester_id`, `roles`, `first_name`, `family_name`, `status_now`, `address`, `email`, `phone`, `date_joined`, `pin`) VALUES (7, 'forester', 'lin', 'lin', 1, 'ddd road', 'ddd@qq.com', '11111111111', '2024-03-02', '05f0a2207618f8d434fa9625e072d8801e888b468751b3b5427638484e5d60c7');
INSERT INTO `forester` (`forester_id`, `roles`, `first_name`, `family_name`, `status_now`, `address`, `email`, `phone`, `date_joined`, `pin`) VALUES (9, 'forester', 'Huizhong', 'Wang', 0, '43 Anaru Road', 'minasopor23@gmail.com', '0204918430', '2024-03-01', 'afae8b1a1bfa4f31753b415fe1aca8e4f32ac2179260c145491a7b6d847b1d04');
INSERT INTO `forester` (`forester_id`, `roles`, `first_name`, `family_name`, `status_now`, `address`, `email`, `phone`, `date_joined`, `pin`) VALUES (10, 'forester', 'Huizhong', 'Wang', 0, '43 Anaru Road', 'minasopor23@gmail.com', '11111111111', '2024-03-13', '4d4a1fce53699e09dd530c2b4805c68427e557c255b14d0e371cc86a524709ad');

INSERT INTO `staff_admin` (`staff_id`, `roles`, `first_name`, `family_name`, `status_now`, `email`, `phone`, `hire_date`, `staff_position`, `department`, `pin`) VALUES (10000, 'admin', 'Jack', 'Smith', 1, '3332qqq@qq', '33333333333', '2019-01-01', 'manager', 'IT', 'b5edf5378bcd60406eca8c096326739b475dcdfcafdc3a4e814ae13346d09f6f');
INSERT INTO `staff_admin` (`staff_id`, `roles`, `first_name`, `family_name`, `status_now`, `email`, `phone`, `hire_date`, `staff_position`, `department`, `pin`) VALUES (10001, 'staff', 'John', 'Chen', 1, 'wewe@ddsfdfdf', '01111111111', '2020-02-02', 'technician', 'IT', 'ad437de2eaae5db4073a5e84fe239fd3c3482bcdaf728530dfe2d0d38e342951');
INSERT INTO `staff_admin` (`staff_id`, `roles`, `first_name`, `family_name`, `status_now`, `email`, `phone`, `hire_date`, `staff_position`, `department`, `pin`) VALUES (10002, 'staff', 'Sally', 'Potter', 1, 'hhh@gmail.com', '11111111111', '2021-03-03', 'technician', 'IT', 'c7e94b9c58e56acb177e3910d0365669bc8804a9df9596e7e430fde44e61cb6a');
INSERT INTO `staff_admin` (`staff_id`, `roles`, `first_name`, `family_name`, `status_now`, `email`, `phone`, `hire_date`, `staff_position`, `department`, `pin`) VALUES (10003, 'staff', 'John', 'Chen', 0, 'ggg@gmail.com', '11111111117', '2020-02-02', 'technician', 'IT', '4d4a1fce53699e09dd530c2b4805c68427e557c255b14d0e371cc86a524709ad');
INSERT INTO `staff_admin` (`staff_id`, `roles`, `first_name`, `family_name`, `status_now`, `email`, `phone`, `hire_date`, `staff_position`, `department`, `pin`) VALUES (10004, 'staff', 'king', 'king', 0, 'WW@QQQ.COM', '32323232', '2024-03-05', 'technician', 'IT', '4d4a1fce53699e09dd530c2b4805c68427e557c255b14d0e371cc86a524709ad');
INSERT INTO `staff_admin` (`staff_id`, `roles`, `first_name`, `family_name`, `status_now`, `email`, `phone`, `hire_date`, `staff_position`, `department`, `pin`) VALUES (10005, 'staff', 'Ki', 'Ki', 1, 'fdsfsf@fsaf.com', '21212121212', '2024-03-01', 'technician', 'IT', '3f7a4272505051b7c574b58f6a2d1efa551d352417dc48b872d70bcebd64fe87');

INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('forester', 1, NULL, '4d4a1fce53699e09dd530c2b4805c68427e557c255b14d0e371cc86a524709ad', 1);
INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('forester', 2, NULL, 'a35206016fbc3b8d77e3f2a6fdae3628e1b852a6bc7a1886b50a4a55fb49fd51', 1);
INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('forester', 3, NULL, '91d2cb6684bd6733a12d286e412d21760796b1d5c2059cd37c51d9fe67a78407', 1);
INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('forester', 4, NULL, 'fcf9415c0f10c6d89fddb6d98fa723483556373f376fec550e71e88cd2d0c4a8', 1);
INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('forester', 5, NULL, 'ce47ce71fb20420e7751eba75e721a3035726b99f1253ede644e433dcf33cb4f', 1);
INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('admin', NULL, 10000, 'b5edf5378bcd60406eca8c096326739b475dcdfcafdc3a4e814ae13346d09f6f', 1);
INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('staff', NULL, 10001, 'ad437de2eaae5db4073a5e84fe239fd3c3482bcdaf728530dfe2d0d38e342951', 1);
INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('staff', NULL, 10002, 'c7e94b9c58e56acb177e3910d0365669bc8804a9df9596e7e430fde44e61cb6a', 1);
INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('staff', NULL, 10003, '4d4a1fce53699e09dd530c2b4805c68427e557c255b14d0e371cc86a524709ad', 0);
INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('forester', 6, NULL, '4d4a1fce53699e09dd530c2b4805c68427e557c255b14d0e371cc86a524709ad', 0);
INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('forester', 7, NULL, '05f0a2207618f8d434fa9625e072d8801e888b468751b3b5427638484e5d60c7', 1);
INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('forester', 9, NULL, 'afae8b1a1bfa4f31753b415fe1aca8e4f32ac2179260c145491a7b6d847b1d04', 0);
INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('forester', 10, NULL, '4d4a1fce53699e09dd530c2b4805c68427e557c255b14d0e371cc86a524709ad', 1);
INSERT INTO `users` (`roles`, `forester_id`, `staff_id`, `pin`, `status_now`) VALUES ('staff', NULL, 10005, '3f7a4272505051b7c574b58f6a2d1efa551d352417dc48b872d70bcebd64fe87', 1);







