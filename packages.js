/* CLI Anything — Package Registry Data */
const S='https://cdn.simpleicons.org/';
const CATEGORIES={
  image:{label:'Image / Design',color:'#6366f1'},
  video:{label:'Video / Audio',color:'#ea580c'},
  '3d':{label:'3D / Gaming',color:'#0891b2'},
  office:{label:'Office / Docs',color:'#16a34a'},
  dev:{label:'Developer Tools',color:'#4f46e5'},
  ai:{label:'AI / ML',color:'#9333ea'},
  comm:{label:'Communication',color:'#0284c7'},
  database:{label:'Database',color:'#b45309'},
  cloud:{label:'Cloud / Infra',color:'#0f766e'},
  browser:{label:'Browser',color:'#c2410c'},
  media:{label:'Media / Entertainment',color:'#7c3aed'},
  gaming:{label:'Gaming',color:'#059669'},
  lifestyle:{label:'Lifestyle / Services',color:'#d946ef'},
};
const CATKEYS=Object.keys(CATEGORIES);

const PACKAGES=[
  // ── Image / Design ──
  {n:"gimp",v:"2.1.0",d:"Image editing, retouching, batch processing, format conversion. Wraps the full GIMP engine.",ld:"Professional-grade raster image editor. Supports layer manipulation, 100+ filters, scripting, and batch processing across 30+ image formats.",c:"image",t:["image","editing","open-source"],dl:"3.2K",ts:187,logo:S+"gimp/5C5543",q:.96,
    caps:["image.open","image.resize","image.filter","image.export","layer.create","layer.merge"],
    cmds:["gimp-cli resize --input photo.png --width 1920","gimp-cli filter --input photo.png --type sharpen","gimp-cli export --input photo.psd --format png"],
    plat:["linux","macos","windows"],req:["gimp>=2.10"],inf:["png","jpg","psd","tiff","bmp","webp"],outf:["png","jpg","webp","tiff"]},

  {n:"photoshop",v:"1.0.0",d:"Adobe Photoshop automation via CLI. Layer operations, filters, batch processing, format conversion.",ld:"Wraps Adobe Photoshop's scripting interface (ExtendScript/UXP) to provide command-line access to professional image editing workflows.",c:"image",t:["adobe","image","editing"],dl:"6.1K",ts:210,logo:null,q:.94,
    caps:["image.open","image.resize","image.filter","image.export","layer.create","layer.style","image.crop","image.adjust"],
    cmds:["photoshop-cli resize --input banner.psd --width 1200 --output json","photoshop-cli export --input design.psd --format png --layers all","photoshop-cli batch --dir ./images --action resize --width 800"],
    plat:["macos","windows"],req:["photoshop>=2024"],inf:["psd","png","jpg","tiff","raw"],outf:["psd","png","jpg","webp","tiff"]},

  {n:"illustrator",v:"1.0.0",d:"Adobe Illustrator vector editing via CLI. Path operations, artboard management, SVG/PDF export.",ld:"Command-line access to Illustrator's vector editing engine. Create, modify, and export vector graphics programmatically.",c:"image",t:["adobe","vector","design"],dl:"2.3K",ts:134,logo:null,q:.91,
    caps:["vector.create","vector.edit","artboard.manage","path.combine","text.set","export.svg","export.pdf"],
    cmds:["illustrator-cli export --input logo.ai --format svg","illustrator-cli artboard --input file.ai --list --output json"],
    plat:["macos","windows"],req:["illustrator>=2024"],inf:["ai","svg","eps","pdf"],outf:["svg","pdf","png","eps"]},

  {n:"figma",v:"2.0.0",d:"Design file inspection, component export, style extraction, library management via Figma API.",ld:"Full Figma REST API wrapper. Inspect designs, export components, extract design tokens, and manage team libraries.",c:"image",t:["design","ui","assets"],dl:"3.8K",ts:178,logo:S+"figma/F24E1E",q:.93,
    caps:["file.inspect","component.export","style.extract","library.manage","comment.read","version.list"],
    cmds:["figma-cli export --file-key abc123 --node-id 1:2 --format png --scale 2","figma-cli styles --file-key abc123 --output json"],
    plat:["linux","macos","windows"],req:["figma-api-token"],inf:["figma"],outf:["png","svg","pdf","jpg"]},

  {n:"inkscape",v:"1.5.2",d:"Vector graphics editing, SVG manipulation, path operations, text-to-path, multi-format export.",ld:"Open-source vector graphics editor. SVG-native with support for path boolean operations, text rendering, and batch export.",c:"image",t:["vector","svg","design"],dl:"1.9K",ts:145,logo:S+"inkscape/000000",q:.92,
    caps:["svg.edit","path.combine","text.topath","export.png","export.pdf","batch.convert"],
    cmds:["inkscape-cli convert --input drawing.svg --format pdf","inkscape-cli export --input logo.svg --format png --dpi 300"],
    plat:["linux","macos","windows"],req:["inkscape>=1.0"],inf:["svg","eps","pdf","ai"],outf:["svg","png","pdf","eps"]},

  {n:"imagemagick",v:"2.4.0",d:"Batch image operations: resize, crop, rotate, composite, format conversion, watermarking.",ld:"The Swiss Army knife of image processing. Supports 200+ image formats, batch operations, and complex compositing.",c:"image",t:["image","batch","conversion"],dl:"4.8K",ts:234,q:.97,
    caps:["image.resize","image.crop","image.rotate","image.composite","image.convert","image.watermark","batch.process"],
    cmds:["imagemagick-cli resize --input photo.jpg --width 800 --height 600","imagemagick-cli convert --input *.png --format webp --quality 85"],
    plat:["linux","macos","windows"],req:["imagemagick>=7"],inf:["png","jpg","gif","tiff","webp","bmp","svg"],outf:["png","jpg","gif","webp","tiff"]},

  {n:"canva",v:"1.0.0",d:"Canva design automation. Create designs from templates, export assets, manage brand kits.",ld:"Wraps Canva's Connect API to automate design creation, template management, and asset export for teams.",c:"image",t:["design","templates","branding"],dl:"1.8K",ts:87,q:.88,
    caps:["design.create","template.list","asset.export","brand.manage"],
    cmds:["canva-cli create --template poster --text 'Hello World' --output poster.png","canva-cli export --design-id abc --format pdf"],
    plat:["linux","macos","windows"],req:["canva-api-token"],inf:["canva"],outf:["png","pdf","jpg","mp4"]},

  // ── Video / Audio ──
  {n:"ffmpeg",v:"3.0.1",d:"Media transcoding, trimming, merging, audio extraction, thumbnail generation, streaming.",ld:"Universal media toolkit. Transcode between any format, extract audio, generate thumbnails, apply filters, and stream.",c:"video",t:["video","audio","transcode"],dl:"5.1K",ts:312,logo:S+"ffmpeg/007808",q:.98,
    caps:["video.transcode","video.trim","video.merge","audio.extract","thumbnail.generate","stream.start","filter.apply"],
    cmds:["ffmpeg-cli transcode --input video.mov --format mp4 --codec h265","ffmpeg-cli trim --input video.mp4 --start 00:01:00 --duration 30","ffmpeg-cli extract-audio --input video.mp4 --format mp3"],
    plat:["linux","macos","windows"],req:["ffmpeg>=5"],inf:["mp4","mov","avi","mkv","webm","flv"],outf:["mp4","webm","mkv","mp3","wav"]},

  {n:"audacity",v:"1.2.1",d:"Audio recording, trimming, effects processing, noise reduction, format conversion.",ld:"Open-source audio editor. Record, trim, apply effects like noise reduction, EQ, compression, and batch convert formats.",c:"video",t:["audio","effects","editing"],dl:"1.5K",ts:98,logo:S+"audacity/0000CC",q:.89,
    caps:["audio.record","audio.trim","audio.effect","noise.reduce","format.convert","batch.process"],
    cmds:["audacity-cli trim --input podcast.wav --start 5 --end 120","audacity-cli denoise --input recording.wav --sensitivity 0.8"],
    plat:["linux","macos","windows"],req:["audacity>=3.0"],inf:["wav","mp3","flac","ogg","aiff"],outf:["wav","mp3","flac","ogg"]},

  {n:"obs-studio",v:"1.4.0",d:"Streaming and recording control. Scene management, source configuration, start/stop streams.",ld:"Control OBS Studio via CLI. Manage scenes, sources, start/stop streams and recordings, configure output settings.",c:"video",t:["streaming","recording","live"],dl:"2.1K",ts:134,logo:S+"obsstudio/302E31",q:.90,
    caps:["stream.start","stream.stop","record.start","record.stop","scene.switch","source.add","output.configure"],
    cmds:["obs-cli stream start --service twitch","obs-cli scene switch --name 'Game Capture'","obs-cli record start --output ./recordings"],
    plat:["linux","macos","windows"],req:["obs-studio>=28"],inf:[],outf:["mp4","mkv","flv"]},

  {n:"premiere-pro",v:"1.0.0",d:"Adobe Premiere Pro video editing. Timeline operations, effects, rendering, and export automation.",ld:"Automate Premiere Pro workflows. Import media, arrange timelines, apply effects, and render final output via CLI.",c:"video",t:["adobe","video","editing"],dl:"3.4K",ts:156,logo:null,q:.91,
    caps:["project.create","timeline.arrange","effect.apply","render.export","media.import","transition.add"],
    cmds:["premiere-cli render --project video.prproj --format mp4 --preset 'YouTube 1080p'","premiere-cli import --project video.prproj --files ./clips/*.mp4"],
    plat:["macos","windows"],req:["premiere-pro>=2024"],inf:["prproj","mp4","mov","mxf"],outf:["mp4","mov","mxf","prores"]},

  {n:"after-effects",v:"1.0.0",d:"Adobe After Effects motion graphics. Composition rendering, expression control, template-based generation.",ld:"Render After Effects compositions via CLI. Control expressions, swap assets, and batch render motion graphics templates.",c:"video",t:["adobe","motion","vfx"],dl:"2.7K",ts:121,logo:null,q:.89,
    caps:["comp.render","expression.set","asset.swap","template.render","output.configure"],
    cmds:["aftereffects-cli render --project intro.aep --comp 'Main' --format mp4","aftereffects-cli template --project mogrt.aep --text 'Breaking News' --output news.mp4"],
    plat:["macos","windows"],req:["after-effects>=2024"],inf:["aep","mogrt"],outf:["mp4","mov","gif","png-sequence"]},

  {n:"kdenlive",v:"1.0.2",d:"Non-linear video editing. Timeline operations, transitions, effects, multi-track rendering.",ld:"Open-source video editor. Script timeline operations, add transitions and effects, render multi-track projects.",c:"video",t:["video","timeline","editing"],dl:"980",ts:112,logo:S+"kdenlive/527EB2",q:.87,
    caps:["timeline.edit","transition.add","effect.apply","render.export","clip.import"],
    cmds:["kdenlive-cli render --project edit.kdenlive --format mp4 --quality high"],
    plat:["linux","macos","windows"],req:["kdenlive>=22"],inf:["kdenlive","mp4","mov"],outf:["mp4","webm","mkv"]},

  {n:"davinci-resolve",v:"1.0.0",d:"DaVinci Resolve editing and color grading. Timeline, color wheels, Fusion, and Fairlight via CLI.",ld:"Professional video editing and color grading. Control timelines, color grading wheels, Fusion VFX, and Fairlight audio.",c:"video",t:["video","color-grading","editing"],dl:"2.9K",ts:167,q:.92,
    caps:["timeline.edit","color.grade","fusion.compose","fairlight.mix","render.export","media.import"],
    cmds:["resolve-cli render --project film.drp --timeline 'Final Cut' --format prores","resolve-cli color --input clip.mp4 --lut cinematic.cube"],
    plat:["linux","macos","windows"],req:["davinci-resolve>=18"],inf:["drp","mp4","mov","mxf","braw"],outf:["mp4","prores","dnxhd","mov"]},

  // ── 3D / Gaming ──
  {n:"blender",v:"1.8.0",d:"3D modeling, scene composition, material application, rendering pipeline and animation export.",ld:"Complete 3D creation suite. Model, sculpt, animate, render, and composite — all from the command line.",c:"3d",t:["3d","rendering","animation"],dl:"2.8K",ts:203,logo:S+"blender/E87D0D",q:.95,
    caps:["model.create","scene.compose","material.apply","render.image","render.animation","sculpt.modify"],
    cmds:["blender-cli render --scene scene.blend --frame 1 --engine cycles","blender-cli export --input model.blend --format glb"],
    plat:["linux","macos","windows"],req:["blender>=3.0"],inf:["blend","obj","fbx","gltf"],outf:["png","exr","fbx","glb","obj"]},

  {n:"unity",v:"1.0.0",d:"Unity engine automation. Build targets, run tests, asset management, batch mode operations.",ld:"Automate Unity workflows. Build for multiple platforms, run unit tests, import assets, and execute batch scripts.",c:"3d",t:["game-engine","build","testing"],dl:"4.1K",ts:189,logo:S+"unity/000000",q:.93,
    caps:["build.target","test.run","asset.import","scene.open","script.execute","package.manage"],
    cmds:["unity-cli build --target android --output ./build/game.apk","unity-cli test --mode editmode --output json"],
    plat:["linux","macos","windows"],req:["unity>=2022"],inf:["unity"],outf:["apk","ipa","exe","app","wasm"]},

  {n:"unreal-engine",v:"1.0.0",d:"Unreal Engine automation. Build, cook, package, and run automated tests via command line.",ld:"Automate Unreal Engine workflows. Build, cook content, package for distribution, and run Gauntlet tests.",c:"3d",t:["game-engine","build","unreal"],dl:"3.2K",ts:145,logo:S+"unrealengine/0E1128",q:.91,
    caps:["build.editor","cook.content","package.game","test.run","plugin.manage","lightmap.build"],
    cmds:["unreal-cli build --platform Win64 --config Shipping","unreal-cli cook --map Level01 --platform Android"],
    plat:["linux","macos","windows"],req:["unreal-engine>=5"],inf:["uproject"],outf:["exe","app","apk","pak"]},

  {n:"godot",v:"1.0.0",d:"Godot engine CLI. Export builds, run tests, manage scenes, and automate game development workflows.",ld:"Open-source game engine automation. Export to multiple platforms, run GDScript tests, and manage project resources.",c:"3d",t:["game-engine","open-source","godot"],dl:"1.9K",ts:98,logo:S+"godotengine/478CBF",q:.88,
    caps:["export.build","test.run","scene.list","resource.import","script.validate"],
    cmds:["godot-cli export --preset 'Linux' --output ./build/game","godot-cli test --script res://tests/"],
    plat:["linux","macos","windows"],req:["godot>=4.0"],inf:["godot","tscn","tres"],outf:["exe","app","apk","html5"]},

  // ── Office / Docs ──
  {n:"microsoft-word",v:"1.0.0",d:"Microsoft Word document automation. Create, edit, format documents, mail merge, PDF export.",ld:"Automate Word via Office JS/COM API. Create documents from templates, apply formatting, run mail merge, and export to PDF.",c:"office",t:["microsoft","documents","word"],dl:"8.2K",ts:234,logo:null,q:.95,
    caps:["doc.create","doc.edit","format.apply","template.use","mailmerge.run","export.pdf","table.insert","image.insert"],
    cmds:["word-cli create --template report.dotx --data data.json --output report.docx","word-cli export --input document.docx --format pdf","word-cli mailmerge --template letter.docx --data contacts.csv"],
    plat:["macos","windows"],req:["microsoft-365"],inf:["docx","dotx","doc","rtf"],outf:["docx","pdf","html","rtf"]},

  {n:"microsoft-excel",v:"1.0.0",d:"Microsoft Excel spreadsheet automation. Data manipulation, formulas, charts, pivot tables, CSV import/export.",ld:"Full Excel automation. Read/write cells, create charts, build pivot tables, run macros, and convert between formats.",c:"office",t:["microsoft","spreadsheet","data"],dl:"9.5K",ts:278,logo:null,q:.96,
    caps:["sheet.read","sheet.write","chart.create","pivot.build","formula.set","macro.run","format.convert","data.filter"],
    cmds:["excel-cli read --input sales.xlsx --sheet 'Q1' --range A1:D100 --output json","excel-cli chart --input data.xlsx --type bar --range B2:D10 --output chart.png","excel-cli convert --input data.csv --format xlsx"],
    plat:["macos","windows"],req:["microsoft-365"],inf:["xlsx","xls","csv","tsv"],outf:["xlsx","csv","pdf","json"]},

  {n:"microsoft-powerpoint",v:"1.0.0",d:"Microsoft PowerPoint automation. Create presentations, apply themes, add content, export slides.",ld:"Automate PowerPoint workflows. Build presentations from templates, insert text/images/charts, apply animations, and export.",c:"office",t:["microsoft","presentation","slides"],dl:"5.8K",ts:189,logo:null,q:.93,
    caps:["slide.create","slide.edit","theme.apply","content.insert","animation.add","export.pdf","export.images"],
    cmds:["powerpoint-cli create --template pitch.potx --data content.json --output deck.pptx","powerpoint-cli export --input slides.pptx --format pdf","powerpoint-cli export --input slides.pptx --format png --slides all"],
    plat:["macos","windows"],req:["microsoft-365"],inf:["pptx","potx","ppt"],outf:["pptx","pdf","png","jpg"]},

  {n:"microsoft-outlook",v:"1.0.0",d:"Microsoft Outlook email automation. Send/read emails, manage calendar, contacts, and folders.",ld:"Automate Outlook via Graph API. Send and search emails, manage calendar events, organize contacts and folders.",c:"office",t:["microsoft","email","calendar"],dl:"4.3K",ts:156,logo:null,q:.92,
    caps:["mail.send","mail.read","mail.search","calendar.create","calendar.list","contact.manage","folder.organize"],
    cmds:["outlook-cli send --to user@email.com --subject 'Report' --body-file report.html --attach data.xlsx","outlook-cli calendar list --start 2026-03-01 --end 2026-03-31 --output json"],
    plat:["macos","windows"],req:["microsoft-365"],inf:["eml","msg","ics"],outf:["json","eml","ics"]},

  {n:"libreoffice",v:"2.3.0",d:"Document, spreadsheet, and presentation automation. Format conversion, mail merge, macro execution.",ld:"Open-source office suite. Create and convert documents, spreadsheets, and presentations. Supports 100+ formats.",c:"office",t:["office","docs","spreadsheet"],dl:"4.0K",ts:156,logo:S+"libreoffice/18A303",q:.94,
    caps:["doc.convert","sheet.read","present.create","macro.run","pdf.export","mailmerge.run"],
    cmds:["libreoffice-cli convert --input report.docx --format pdf","libreoffice-cli convert --input *.odt --format docx --batch"],
    plat:["linux","macos","windows"],req:["libreoffice>=7"],inf:["odt","docx","xlsx","pptx","csv"],outf:["pdf","docx","xlsx","html"]},

  {n:"google-docs",v:"1.0.0",d:"Google Docs automation via API. Create, edit, format documents, insert content, export.",ld:"Create and manipulate Google Docs via the Google Workspace API. Template-based generation, collaborative editing, multi-format export.",c:"office",t:["google","documents","cloud"],dl:"3.9K",ts:145,logo:S+"googledocs/4285F4",q:.91,
    caps:["doc.create","doc.edit","template.merge","content.insert","export.pdf","share.manage"],
    cmds:["gdocs-cli create --title 'Monthly Report' --template-id abc123 --data report.json","gdocs-cli export --doc-id xyz --format pdf"],
    plat:["linux","macos","windows"],req:["google-api-credentials"],inf:["gdoc"],outf:["docx","pdf","html","txt"]},

  {n:"google-sheets",v:"1.0.0",d:"Google Sheets automation. Read/write data, create charts, manage formulas, import/export CSV.",ld:"Full Google Sheets API wrapper. Read and write spreadsheet data, manage formulas, create charts, and sync with external data.",c:"office",t:["google","spreadsheet","data"],dl:"4.7K",ts:167,logo:S+"googlesheets/34A853",q:.93,
    caps:["sheet.read","sheet.write","chart.create","formula.set","data.import","share.manage"],
    cmds:["gsheets-cli read --id abc123 --range 'Sheet1!A1:D100' --output json","gsheets-cli write --id abc123 --range A1 --data data.csv"],
    plat:["linux","macos","windows"],req:["google-api-credentials"],inf:["csv","json"],outf:["csv","json","xlsx","pdf"]},

  {n:"keynote",v:"1.1.0",d:"Presentation creation, slide management, theme application, export to PDF, PPTX, and images.",ld:"macOS Keynote automation via AppleScript. Create presentations, manage slides, apply themes, and export to multiple formats.",c:"office",t:["presentations","macos","slides"],dl:"1.2K",ts:89,q:.87,
    caps:["slide.create","slide.edit","theme.apply","export.pdf","export.pptx","export.images"],
    cmds:["keynote-cli export --input presentation.key --format pdf","keynote-cli create --template modern --data slides.json"],
    plat:["macos"],req:["keynote>=13"],inf:["key"],outf:["pdf","pptx","png","jpg"]},

  {n:"notion",v:"1.7.0",d:"Page creation, database queries, block manipulation, content search, workspace management.",ld:"Full Notion API wrapper. Create pages, query databases, manipulate blocks, search content, and manage workspace.",c:"office",t:["docs","database","wiki"],dl:"4.5K",ts:167,logo:S+"notion/000000",q:.93,
    caps:["page.create","page.update","database.query","block.append","search.content","user.list"],
    cmds:["notion-cli query --database-id abc123 --filter '{\"Status\":\"Done\"}' --output json","notion-cli create-page --parent abc --title 'Meeting Notes' --content notes.md"],
    plat:["linux","macos","windows"],req:["notion-api-token"],inf:["md","json"],outf:["json","md"]},

  {n:"pandoc",v:"1.9.0",d:"Universal document converter. Markdown, LaTeX, DOCX, HTML, PDF, EPUB inter-conversion.",ld:"The universal document converter. Convert between 40+ document formats including Markdown, LaTeX, Word, HTML, PDF, and EPUB.",c:"office",t:["documents","conversion","markdown"],dl:"3.6K",ts:167,q:.95,
    caps:["doc.convert","template.apply","filter.run","metadata.set","toc.generate","cite.process"],
    cmds:["pandoc-cli convert --input paper.md --format pdf --template academic","pandoc-cli convert --input book.epub --format docx"],
    plat:["linux","macos","windows"],req:["pandoc>=3.0"],inf:["md","tex","docx","html","epub","rst"],outf:["pdf","docx","html","epub","tex"]},

  // ── Communication ──
  {n:"slack",v:"1.6.0",d:"Message sending, channel management, file handling, conversation search, webhook integration.",ld:"Full Slack API wrapper. Send messages, manage channels, upload files, search conversations, and configure webhooks.",c:"comm",t:["messaging","workspace","api"],dl:"3.1K",ts:142,logo:S+"slack/4A154B",q:.92,
    caps:["message.send","message.search","channel.create","channel.list","file.upload","user.list","webhook.send"],
    cmds:["slack-cli send --channel '#general' --text 'Deploy complete'","slack-cli search --query 'bug report' --output json"],
    plat:["linux","macos","windows"],req:["slack-bot-token"],inf:["txt","json"],outf:["json"]},

  {n:"microsoft-teams",v:"1.0.0",d:"Microsoft Teams automation. Send messages, manage channels, schedule meetings, handle files.",ld:"Automate Teams via Graph API. Post messages, create channels, schedule meetings, and manage team files.",c:"comm",t:["microsoft","messaging","meetings"],dl:"5.2K",ts:178,logo:null,q:.91,
    caps:["message.send","channel.create","meeting.schedule","file.share","team.manage","chat.create"],
    cmds:["teams-cli send --team 'Engineering' --channel 'General' --text 'Build passed'","teams-cli meeting --title 'Standup' --time '2026-03-16T10:00' --attendees team.txt"],
    plat:["linux","macos","windows"],req:["microsoft-365"],inf:["txt","json"],outf:["json"]},

  {n:"zoom",v:"1.0.0",d:"Zoom meeting automation. Schedule, start, manage meetings, download recordings, manage participants.",ld:"Control Zoom via REST API. Schedule meetings, manage participants, retrieve recordings, and configure room settings.",c:"comm",t:["meetings","video","conferencing"],dl:"4.8K",ts:134,logo:S+"zoom/0B5CFF",q:.90,
    caps:["meeting.schedule","meeting.start","meeting.end","recording.download","participant.manage","webinar.create"],
    cmds:["zoom-cli schedule --topic 'Sprint Review' --time '2026-03-16T14:00' --duration 60","zoom-cli recordings --from 2026-03-01 --output json"],
    plat:["linux","macos","windows"],req:["zoom-api-credentials"],inf:[],outf:["json","mp4"]},

  {n:"discord",v:"1.0.0",d:"Discord bot operations. Send messages, manage servers, handle roles, moderate channels.",ld:"Full Discord Bot API wrapper. Post messages with embeds, manage server roles and channels, handle moderation.",c:"comm",t:["messaging","gaming","community"],dl:"3.6K",ts:156,logo:S+"discord/5865F2",q:.91,
    caps:["message.send","message.embed","channel.create","role.manage","server.info","moderation.ban"],
    cmds:["discord-cli send --channel 123456 --text 'Server update deployed'","discord-cli roles --server 789 --list --output json"],
    plat:["linux","macos","windows"],req:["discord-bot-token"],inf:["txt","json"],outf:["json"]},

  {n:"telegram",v:"1.0.0",d:"Telegram bot operations. Send messages, manage groups, handle media, set up webhooks.",ld:"Telegram Bot API wrapper. Send text/media messages, manage groups, handle inline queries, and configure webhooks.",c:"comm",t:["messaging","bots","api"],dl:"2.8K",ts:112,logo:S+"telegram/26A5E4",q:.90,
    caps:["message.send","media.send","group.manage","webhook.set","inline.handle","poll.create"],
    cmds:["telegram-cli send --chat 123 --text 'Alert: server down'","telegram-cli send --chat 123 --photo screenshot.png"],
    plat:["linux","macos","windows"],req:["telegram-bot-token"],inf:["txt","json","png","jpg","mp4"],outf:["json"]},

  {n:"whatsapp",v:"1.0.0",d:"WhatsApp Business API. Send messages, manage templates, handle media, automate customer communication.",ld:"WhatsApp Business Cloud API wrapper. Send template messages, handle media, manage contacts, and automate replies.",c:"comm",t:["messaging","business","api"],dl:"3.4K",ts:98,logo:S+"whatsapp/25D366",q:.88,
    caps:["message.send","template.send","media.upload","contact.manage","webhook.configure"],
    cmds:["whatsapp-cli send --to +1234567890 --template order_confirmation --params '{\"order\":\"#123\"}'"],
    plat:["linux","macos","windows"],req:["whatsapp-business-api"],inf:["json","txt"],outf:["json"]},

  {n:"wechat",v:"1.0.0",d:"WeChat Official Account & Mini Program management. Send messages, manage menus, handle events.",ld:"WeChat Official Account Platform API wrapper. Manage followers, send template messages, customize menus, and handle events.",c:"comm",t:["messaging","china","wechat"],dl:"2.1K",ts:87,logo:S+"wechat/07C160",q:.86,
    caps:["message.send","menu.set","follower.list","template.send","media.upload","qrcode.create"],
    cmds:["wechat-cli send --template order_notify --user open_id --data '{\"status\":\"shipped\"}'"],
    plat:["linux","macos","windows"],req:["wechat-app-id"],inf:["json"],outf:["json"]},

  {n:"gmail",v:"1.0.0",d:"Gmail automation via API. Send, read, search emails, manage labels, handle attachments.",ld:"Google Gmail API wrapper. Compose and send emails, search inbox, manage labels, download attachments, and handle drafts.",c:"comm",t:["google","email","automation"],dl:"5.1K",ts:178,logo:S+"gmail/EA4335",q:.93,
    caps:["mail.send","mail.read","mail.search","label.manage","attachment.download","draft.create","filter.set"],
    cmds:["gmail-cli send --to user@email.com --subject 'Report' --body-file email.html --attach report.pdf","gmail-cli search --query 'from:boss subject:urgent' --output json"],
    plat:["linux","macos","windows"],req:["google-api-credentials"],inf:["eml","html","txt"],outf:["json","eml"]},

  // ── Developer Tools ──
  {n:"docker",v:"2.5.0",d:"Container lifecycle, compose orchestration, image building, network configuration, log streaming.",ld:"Enhanced Docker management. Orchestrate containers, build images, manage networks, and stream logs with structured output.",c:"dev",t:["containers","devops","cloud"],dl:"6.2K",ts:256,logo:S+"docker/2496ED",q:.97,
    caps:["container.run","container.stop","image.build","image.push","compose.up","network.create","log.stream"],
    cmds:["docker-cli compose up --file docker-compose.yml --detach","docker-cli build --tag myapp:latest --output json"],
    plat:["linux","macos","windows"],req:["docker>=20"],inf:["Dockerfile","docker-compose.yml"],outf:["json"]},

  {n:"vscode",v:"1.0.0",d:"VS Code automation. Extension management, settings, workspace operations, task running.",ld:"Automate Visual Studio Code. Install extensions, modify settings, manage workspaces, run tasks, and control the editor.",c:"dev",t:["editor","ide","extensions"],dl:"4.5K",ts:189,logo:null,q:.94,
    caps:["extension.install","extension.list","settings.modify","workspace.open","task.run","diff.view"],
    cmds:["vscode-cli extension install ms-python.python","vscode-cli settings set editor.fontSize 14 --output json"],
    plat:["linux","macos","windows"],req:["vscode>=1.80"],inf:["json"],outf:["json"]},

  {n:"git",v:"2.0.0",d:"Enhanced Git operations. Semantic commits, branch management, conflict resolution, changelog generation.",ld:"Enhanced Git wrapper with structured output. Semantic commits, smart branch management, conflict analysis, and changelog generation.",c:"dev",t:["version-control","git","collaboration"],dl:"7.8K",ts:312,logo:S+"git/F05032",q:.97,
    caps:["commit.semantic","branch.manage","conflict.analyze","changelog.generate","tag.create","stash.manage"],
    cmds:["git-cli commit --type feat --scope auth --message 'add OAuth2 support'","git-cli changelog --from v1.0 --to v2.0 --format md"],
    plat:["linux","macos","windows"],req:["git>=2.30"],inf:[],outf:["json","md"]},

  {n:"kubernetes",v:"1.0.0",d:"Kubernetes cluster management. Deploy, scale, monitor pods, manage services and configs.",ld:"Enhanced kubectl wrapper. Deploy applications, scale services, inspect pods, manage configs, and monitor cluster health.",c:"dev",t:["containers","orchestration","k8s"],dl:"5.6K",ts:234,logo:S+"kubernetes/326CE5",q:.95,
    caps:["pod.deploy","pod.scale","service.expose","config.manage","log.stream","cluster.info","rollout.manage"],
    cmds:["k8s-cli deploy --image myapp:v2 --replicas 3 --namespace prod","k8s-cli pods --namespace prod --status --output json"],
    plat:["linux","macos","windows"],req:["kubectl>=1.25"],inf:["yaml","json"],outf:["json","yaml"]},

  {n:"drawio",v:"1.2.0",d:"Diagram generation: flowcharts, UML, ER diagrams, network topologies. Multi-format export.",ld:"Create and edit diagrams programmatically. Flowcharts, UML, ER, network diagrams with multiple export formats.",c:"dev",t:["diagrams","flowchart","uml"],dl:"1.8K",ts:95,logo:S+"diagramsdotnet/F08705",q:.88,
    caps:["diagram.create","diagram.edit","export.png","export.svg","export.pdf","template.use"],
    cmds:["drawio-cli export --input architecture.drawio --format svg","drawio-cli create --template flowchart --data flow.json"],
    plat:["linux","macos","windows"],req:["drawio>=20"],inf:["drawio","xml"],outf:["png","svg","pdf","xml"]},

  {n:"postman",v:"1.0.0",d:"API testing automation. Run collections, environment management, assertions, report generation.",ld:"Run Postman collections from CLI. Execute API tests, manage environments, validate responses, and generate reports.",c:"dev",t:["api","testing","http"],dl:"4.2K",ts:178,logo:S+"postman/FF6C37",q:.93,
    caps:["collection.run","environment.set","assertion.validate","report.generate","mock.create"],
    cmds:["postman-cli run --collection api-tests.json --environment prod.json --output json","postman-cli run --collection smoke.json --reporters html,json"],
    plat:["linux","macos","windows"],req:["postman-api-key"],inf:["json"],outf:["json","html"]},

  {n:"github",v:"2.0.0",d:"GitHub operations. Repository management, issues, pull requests, Actions, releases, and more.",ld:"Enhanced GitHub CLI wrapper. Manage repos, issues, PRs, Actions workflows, releases, and organization settings.",c:"dev",t:["git","collaboration","ci-cd"],dl:"8.1K",ts:289,logo:S+"github/181717",q:.97,
    caps:["repo.create","issue.create","pr.create","pr.review","action.trigger","release.create","org.manage"],
    cmds:["github-cli pr create --title 'Feature X' --body 'Description' --output json","github-cli actions run --workflow deploy.yml --ref main"],
    plat:["linux","macos","windows"],req:["github-token"],inf:["json","md"],outf:["json"]},

  {n:"jira",v:"1.0.0",d:"Jira project management. Create issues, manage sprints, track progress, generate reports.",ld:"Atlassian Jira API wrapper. Create and manage issues, plan sprints, track progress, and generate burndown reports.",c:"dev",t:["project-management","agile","atlassian"],dl:"3.8K",ts:145,logo:S+"jira/0052CC",q:.91,
    caps:["issue.create","issue.update","sprint.manage","board.view","report.generate","search.jql"],
    cmds:["jira-cli create --project ENG --type story --summary 'Implement login' --output json","jira-cli search --jql 'sprint = current AND status = \"In Progress\"' --output json"],
    plat:["linux","macos","windows"],req:["jira-api-token"],inf:["json"],outf:["json"]},

  // ── AI / ML ──
  {n:"tesseract",v:"1.3.0",d:"Multi-language OCR, layout analysis, table detection, confidence scoring, PDF text extraction.",ld:"Advanced OCR pipeline. Extract text from images in 100+ languages, detect layouts, find tables, and process PDFs.",c:"ai",t:["ocr","text-extraction","ml"],dl:"2.4K",ts:121,q:.91,
    caps:["ocr.extract","layout.analyze","table.detect","pdf.extract","language.detect","confidence.score"],
    cmds:["tesseract-cli extract --input scan.png --lang eng+chi --output json","tesseract-cli pdf --input document.pdf --pages 1-5 --output text"],
    plat:["linux","macos","windows"],req:["tesseract>=5"],inf:["png","jpg","tiff","pdf"],outf:["json","txt","hocr"]},

  {n:"stable-diffusion",v:"1.5.0",d:"AI image generation: txt2img, img2img, inpainting, ControlNet support, model management.",ld:"Generate images with Stable Diffusion models. Text-to-image, image-to-image, inpainting, ControlNet, LoRA management.",c:"ai",t:["generation","diffusion","models"],dl:"7.3K",ts:198,q:.92,
    caps:["txt2img.generate","img2img.transform","inpaint.fill","controlnet.apply","model.load","lora.apply"],
    cmds:["sd-cli generate --prompt 'a cat wearing a hat' --size 1024x1024 --output cat.png","sd-cli img2img --input sketch.png --prompt 'oil painting style' --strength 0.7"],
    plat:["linux","macos","windows"],req:["python>=3.10","torch>=2.0"],inf:["png","jpg","txt"],outf:["png","jpg","webp"]},

  {n:"whisper",v:"1.2.0",d:"Speech-to-text transcription, language detection, timestamp generation, subtitle export.",ld:"OpenAI Whisper speech recognition. Transcribe audio in 99 languages, detect language, generate timestamps and subtitles.",c:"ai",t:["speech","transcription","ml"],dl:"5.9K",ts:143,q:.94,
    caps:["transcribe.audio","language.detect","timestamp.generate","subtitle.export","translate.english"],
    cmds:["whisper-cli transcribe --input meeting.mp3 --language auto --output json","whisper-cli subtitle --input podcast.wav --format srt"],
    plat:["linux","macos","windows"],req:["python>=3.10","whisper"],inf:["mp3","wav","m4a","flac","ogg"],outf:["json","txt","srt","vtt"]},

  // ── Database ──
  {n:"postgres",v:"2.0.0",d:"Database management, query execution, schema inspection, backup/restore, migration tools.",ld:"Enhanced PostgreSQL management. Execute queries with JSON output, inspect schemas, manage backups, and run migrations.",c:"database",t:["database","sql","backup"],dl:"5.4K",ts:289,logo:S+"postgresql/4169E1",q:.97,
    caps:["query.execute","schema.inspect","backup.create","backup.restore","migration.run","index.manage","role.manage"],
    cmds:["postgres-cli query --db myapp --sql 'SELECT * FROM users LIMIT 10' --output json","postgres-cli backup --db myapp --output backup.sql.gz"],
    plat:["linux","macos","windows"],req:["postgresql>=14"],inf:["sql"],outf:["json","csv","sql"]},

  {n:"mysql",v:"1.0.0",d:"MySQL database management. Query execution, schema inspection, backup, replication monitoring.",ld:"Enhanced MySQL management. Execute queries, inspect table schemas, create backups, and monitor replication status.",c:"database",t:["database","sql","mysql"],dl:"4.8K",ts:234,logo:S+"mysql/4479A1",q:.95,
    caps:["query.execute","schema.inspect","backup.create","backup.restore","replication.status","user.manage"],
    cmds:["mysql-cli query --db shop --sql 'SELECT * FROM orders WHERE status=\"pending\"' --output json","mysql-cli backup --db shop --compress --output shop.sql.gz"],
    plat:["linux","macos","windows"],req:["mysql>=8"],inf:["sql"],outf:["json","csv","sql"]},

  {n:"mongodb",v:"1.0.0",d:"MongoDB operations. Query, aggregate, index management, backup/restore, collection management.",ld:"Enhanced MongoDB management. Execute queries and aggregations, manage indexes, create backups, and administer collections.",c:"database",t:["database","nosql","mongodb"],dl:"4.1K",ts:198,logo:S+"mongodb/47A248",q:.94,
    caps:["query.find","query.aggregate","index.create","backup.create","collection.manage","user.manage"],
    cmds:["mongo-cli find --db myapp --collection users --filter '{\"active\":true}' --output json","mongo-cli aggregate --db analytics --collection events --pipeline pipeline.json"],
    plat:["linux","macos","windows"],req:["mongodb>=6"],inf:["json"],outf:["json","csv"]},

  {n:"redis",v:"1.0.0",d:"Redis data management. Key operations, pub/sub, cluster management, memory analysis.",ld:"Enhanced Redis management. Execute commands, manage pub/sub, monitor cluster health, and analyze memory usage.",c:"database",t:["database","cache","redis"],dl:"3.5K",ts:167,logo:S+"redis/DC382D",q:.93,
    caps:["key.get","key.set","key.scan","pubsub.publish","cluster.info","memory.analyze","backup.create"],
    cmds:["redis-cli get --key user:123 --output json","redis-cli scan --pattern 'session:*' --count --output json"],
    plat:["linux","macos","windows"],req:["redis>=7"],inf:[],outf:["json"]},

  // ── Cloud / Infra ──
  {n:"aws-cli",v:"2.0.0",d:"AWS service management. S3, EC2, Lambda, CloudFormation, IAM — unified structured output.",ld:"Enhanced AWS CLI wrapper. Manage S3 buckets, EC2 instances, Lambda functions, and CloudFormation stacks with JSON output.",c:"cloud",t:["aws","cloud","infrastructure"],dl:"8.9K",ts:345,logo:S+"amazonwebservices/232F3E",q:.97,
    caps:["s3.sync","ec2.manage","lambda.deploy","cf.deploy","iam.manage","rds.manage","cloudwatch.query"],
    cmds:["aws-cli s3 sync --source ./build --bucket my-app --delete","aws-cli lambda deploy --function api --zip package.zip --output json"],
    plat:["linux","macos","windows"],req:["aws-cli>=2"],inf:["json","yaml"],outf:["json"]},

  {n:"gcloud",v:"1.0.0",d:"Google Cloud Platform management. Compute, Storage, Cloud Run, BigQuery, IAM operations.",ld:"Enhanced Google Cloud CLI. Manage Compute Engine, Cloud Storage, Cloud Run, BigQuery, and IAM with structured output.",c:"cloud",t:["gcp","cloud","infrastructure"],dl:"6.2K",ts:278,logo:S+"googlecloud/4285F4",q:.95,
    caps:["compute.manage","storage.sync","run.deploy","bigquery.query","iam.manage","pubsub.manage"],
    cmds:["gcloud-cli run deploy --image gcr.io/myapp --region us-central1 --output json","gcloud-cli bigquery --query 'SELECT * FROM dataset.table LIMIT 100' --output json"],
    plat:["linux","macos","windows"],req:["gcloud-sdk"],inf:["json","yaml"],outf:["json"]},

  {n:"azure-cli",v:"1.0.0",d:"Microsoft Azure management. VMs, Storage, Functions, AKS, and resource group operations.",ld:"Enhanced Azure CLI. Manage Virtual Machines, Blob Storage, Azure Functions, AKS clusters, and resource groups.",c:"cloud",t:["azure","cloud","infrastructure"],dl:"5.1K",ts:234,logo:null,q:.94,
    caps:["vm.manage","storage.sync","function.deploy","aks.manage","resource.group","sql.manage"],
    cmds:["azure-cli function deploy --name api --package ./dist --output json","azure-cli vm list --resource-group prod --output json"],
    plat:["linux","macos","windows"],req:["azure-cli>=2"],inf:["json","yaml"],outf:["json"]},

  {n:"cloudflare",v:"1.0.0",d:"Cloudflare management. DNS, Workers, Pages, R2 storage, WAF rules, and analytics.",ld:"Manage Cloudflare services. Configure DNS records, deploy Workers, manage Pages, R2 storage, and WAF rules.",c:"cloud",t:["cdn","dns","edge"],dl:"3.8K",ts:156,logo:S+"cloudflare/F38020",q:.92,
    caps:["dns.manage","worker.deploy","pages.deploy","r2.manage","waf.configure","analytics.query"],
    cmds:["cloudflare-cli worker deploy --name api --script worker.js","cloudflare-cli dns set --zone example.com --type A --name @ --content 1.2.3.4"],
    plat:["linux","macos","windows"],req:["cloudflare-api-token"],inf:["js","json"],outf:["json"]},

  {n:"terraform",v:"1.0.0",d:"Infrastructure as Code. Plan, apply, destroy, state management, module operations.",ld:"Enhanced Terraform wrapper. Plan and apply infrastructure changes, manage state, and work with modules — all with structured output.",c:"cloud",t:["iac","devops","infrastructure"],dl:"5.9K",ts:267,logo:S+"terraform/844FBA",q:.96,
    caps:["plan.run","apply.run","destroy.run","state.manage","module.install","output.read","workspace.manage"],
    cmds:["terraform-cli plan --output json","terraform-cli apply --auto-approve --output json"],
    plat:["linux","macos","windows"],req:["terraform>=1.5"],inf:["tf","hcl","json"],outf:["json"]},

  // ── Browser ──
  {n:"chrome",v:"1.0.0",d:"Chrome browser automation. Page navigation, screenshots, PDF generation, network monitoring.",ld:"Control Chrome via DevTools Protocol. Navigate pages, take screenshots, generate PDFs, intercept network, and run JavaScript.",c:"browser",t:["browser","automation","testing"],dl:"6.5K",ts:234,logo:S+"googlechrome/4285F4",q:.95,
    caps:["page.navigate","page.screenshot","page.pdf","network.intercept","js.execute","cookie.manage","console.capture"],
    cmds:["chrome-cli screenshot --url https://example.com --output page.png --width 1920","chrome-cli pdf --url https://example.com --output page.pdf"],
    plat:["linux","macos","windows"],req:["chrome>=120"],inf:["url"],outf:["png","pdf","json","html"]},

  {n:"firefox",v:"1.0.0",d:"Firefox browser automation. Web testing, screenshots, HAR export, accessibility auditing.",ld:"Control Firefox via Marionette/WebDriver. Automate browsing, capture screenshots, export HAR files, and audit accessibility.",c:"browser",t:["browser","automation","testing"],dl:"3.2K",ts:167,logo:S+"firefox/FF7139",q:.91,
    caps:["page.navigate","page.screenshot","har.export","a11y.audit","cookie.manage","console.capture"],
    cmds:["firefox-cli screenshot --url https://example.com --output page.png","firefox-cli a11y --url https://example.com --output report.json"],
    plat:["linux","macos","windows"],req:["firefox>=120"],inf:["url"],outf:["png","json","har"]},

  {n:"safari",v:"1.0.0",d:"Safari browser automation on macOS. Web testing, screenshots, performance profiling.",ld:"Control Safari via WebDriver. Automate web testing, capture screenshots, and profile page performance on macOS.",c:"browser",t:["browser","macos","testing"],dl:"1.8K",ts:89,logo:S+"safari/006CFF",q:.86,
    caps:["page.navigate","page.screenshot","performance.profile","cookie.manage"],
    cmds:["safari-cli screenshot --url https://example.com --output page.png","safari-cli profile --url https://example.com --output perf.json"],
    plat:["macos"],req:["safari>=17"],inf:["url"],outf:["png","json"]},

  // ── New: Video / Audio ──
  {n:"shotcut",v:"1.0.0",d:"Open-source video editor. Timeline editing, 17 built-in filters, multi-format rendering via MLT.",ld:"CLI for Shotcut video editor. Create and manipulate MLT XML projects, add tracks, place clips, apply video/audio filters, set transitions, and render via melt or ffmpeg.",c:"video",t:["video","editing","open-source"],dl:"1.2K",ts:144,logo:S+"shotcut/115C77",q:.88,
    caps:["project.create","timeline.edit","clip.add","filter.apply","export.render","media.probe"],
    cmds:["shotcut-cli project new --profile hd1080p30","shotcut-cli timeline add-clip video.mp4 --track 1 --in 00:00:05.000 --out 00:00:15.000","shotcut-cli filter add brightness --track 1 --clip 0 --param level=1.15","shotcut-cli export render output.mp4 --preset h264-high"],
    plat:["linux","macos","windows"],req:["shotcut>=22","ffmpeg"],inf:["mp4","mov","mkv","webm","avi"],outf:["mp4","webm","mkv","gif","prores"]},

  // ── New: Office / Docs ──
  {n:"wps-office",v:"1.0.0",d:"WPS Office automation via COM. Writer, Spreadsheets, Presentation — create, edit, export to PDF.",ld:"Automate WPS Office programmatically. Control WPS Writer, Spreadsheets (ET), and Presentation (WPP). Create documents, write cells, export to PDF, and convert between formats.",c:"office",t:["office","wps","documents"],dl:"2.3K",ts:156,logo:null,q:.90,
    caps:["writer.create","writer.edit","writer.export","calc.write","calc.read","impress.create","convert.pdf"],
    cmds:["wps-cli writer new --output report.docx --title 'Q4 Report'","wps-cli calc write-cell data.xlsx --cell A1 --value 'Revenue' --sheet Sheet1","wps-cli impress new --output slides.pptx --title 'Strategy'","wps-cli writer to-pdf report.docx --output report.pdf"],
    plat:["windows"],req:["wps-office>=12"],inf:["docx","xlsx","pptx","doc","xls"],outf:["docx","xlsx","pptx","pdf"]},

  {n:"ms365",v:"1.0.0",d:"Microsoft 365 unified CLI. Word, Excel, PowerPoint, Outlook automation via COM interface.",ld:"Unified CLI for Microsoft 365 Office automation. Control Word, Excel, PowerPoint, and Outlook programmatically — create documents, read/write cells, export to PDF, send emails, and manage calendar.",c:"office",t:["microsoft","office","unified"],dl:"7.5K",ts:312,logo:null,q:.95,
    caps:["word.create","word.edit","excel.write","excel.read","powerpoint.create","outlook.send","outlook.calendar","convert.pdf"],
    cmds:["ms365-cli word new --output report.docx --title 'Q4 Report'","ms365-cli excel write-cell data.xlsx --cell A1 --value 'Revenue'","ms365-cli powerpoint new --output deck.pptx --title 'Strategy'","ms365-cli outlook send --to user@company.com --subject 'Update' --body 'See attached'"],
    plat:["windows","macos"],req:["microsoft-365"],inf:["docx","xlsx","pptx","csv"],outf:["docx","xlsx","pptx","pdf"]},

  {n:"google-workspace",v:"1.0.0",d:"Google Workspace unified CLI. Drive, Gmail, Calendar, Sheets, Docs, and Chat in one tool.",ld:"Unified CLI for Google Workspace APIs. Manage Google Drive files, send Gmail, schedule Calendar events, read/write Sheets, create Docs, and send Chat messages. Supports OAuth2 and service accounts.",c:"office",t:["google","workspace","cloud"],dl:"4.2K",ts:198,logo:S+"google/4285F4",q:.93,
    caps:["drive.manage","gmail.send","gmail.search","calendar.events","sheets.read","sheets.write","docs.create","chat.send"],
    cmds:["gworkspace-cli drive list --limit 20","gworkspace-cli gmail send --to user@example.com --subject 'Report' --body 'Attached'","gworkspace-cli calendar events --days 7","gworkspace-cli sheets read SPREADSHEET_ID 'Sheet1!A1:C10'"],
    plat:["linux","macos","windows"],req:["google-api-credentials"],inf:["json","csv"],outf:["json","csv","pdf"]},

  // ── New: Communication ──
  {n:"feishu",v:"1.0.0",d:"Feishu/Lark enterprise platform. Messaging, documents, calendar, group management via open API.",ld:"CLI for Feishu (Lark) open platform. Send messages and rich cards, manage groups, create documents, schedule calendar events, query users, and send notification cards with severity levels.",c:"comm",t:["messaging","enterprise","feishu"],dl:"1.8K",ts:134,logo:S+"lark/00D6B9",q:.89,
    caps:["message.send","card.send","group.manage","doc.create","calendar.manage","user.search","notify.send"],
    cmds:["feishu-cli msg send --to OPEN_ID --text 'Hello from CLI'","feishu-cli msg send-card --to CHAT_ID --title 'Deploy Complete' --body 'v2.1 is live' --color green","feishu-cli cal list --start 2026-01-01 --end 2026-01-07","feishu-cli doc create --title 'Meeting Notes' --content '# Agenda'"],
    plat:["linux","macos","windows"],req:["feishu-app-credentials"],inf:["json","md"],outf:["json"]},

  {n:"twilio",v:"1.0.0",d:"Twilio communications API. Send SMS, make voice calls, send WhatsApp messages, manage phone numbers.",ld:"CLI for Twilio REST API. Send SMS and WhatsApp messages, initiate voice calls with TwiML, list message and call history, and manage owned phone numbers.",c:"comm",t:["sms","voice","api"],dl:"2.4K",ts:112,logo:S+"twilio/F22F46",q:.90,
    caps:["sms.send","sms.list","call.make","call.list","whatsapp.send","number.list"],
    cmds:["twilio-cli sms send --to +15551234567 --from +15559876543 --body 'Hello from CLI'","twilio-cli calls make --to +15551234567 --from +15559876543 --twiml '<Response><Say>Hello</Say></Response>'","twilio-cli whatsapp send --to +15551234567 --body 'Hello via WhatsApp'"],
    plat:["linux","macos","windows"],req:["twilio-credentials"],inf:["txt","json"],outf:["json"]},

  // ── New: AI / ML ──
  {n:"ollama",v:"1.0.0",d:"Ollama local LLM management. Pull models, generate text, multi-turn chat, embeddings.",ld:"CLI for Ollama local LLM server. Manage models (pull, list, delete, copy), run single-turn text generation, multi-turn ChatML conversations, and generate embedding vectors. JSON-first output for agent integration.",c:"ai",t:["llm","local","inference"],dl:"6.8K",ts:178,logo:S+"ollama/000000",q:.94,
    caps:["model.list","model.pull","model.delete","generate.text","chat.multi","embeddings.generate","server.detect"],
    cmds:["ollama-cli list --json","ollama-cli pull llama3.2","ollama-cli run llama3.2 'Explain quantum computing in one sentence'","ollama-cli chat llama3.2 --message 'system:You are a concise assistant' --message 'user:What is 2+2?'","ollama-cli embeddings nomic-embed-text 'Hello world' --json"],
    plat:["linux","macos","windows"],req:["ollama"],inf:["txt","json"],outf:["json","txt"]},

  {n:"anygen",v:"1.0.0",d:"AnyGen AI content generation. Create slides, documents, diagrams, websites, and data reports via API.",ld:"CLI for AnyGen cloud content generation platform. Create professional presentations (PPTX), documents (DOCX), SmartDraw diagrams, websites, storybooks, and data analysis reports. Full async workflow: create task, poll status, download output.",c:"ai",t:["generation","slides","documents"],dl:"1.5K",ts:98,q:.87,
    caps:["task.create","task.poll","task.download","file.upload","session.manage","prepare.analyze"],
    cmds:["anygen-cli task run --operation slide --prompt 'Create a quarterly business review' --output ./","anygen-cli task create --operation doc --prompt 'Write a PRD for a mobile app'","anygen-cli task create --operation smart_draw --prompt 'Architecture diagram for microservices'","anygen-cli task status TASK_ID"],
    plat:["linux","macos","windows"],req:["anygen-api-key"],inf:["pdf","json","txt"],outf:["pptx","docx","drawio","png"]},

  // ── New: Cloud / Infra ──
  {n:"hubspot",v:"1.0.0",d:"HubSpot CRM management. Contacts, deals, companies — search, create, and manage CRM records.",ld:"CLI for HubSpot CRM REST API. Manage contacts (list, search, create), deals (list, create with pipeline stages), and companies (list, search by domain). Full JSON output for agent integration.",c:"cloud",t:["crm","sales","marketing"],dl:"1.9K",ts:87,logo:S+"hubspot/FF7A59",q:.88,
    caps:["contact.list","contact.search","contact.create","deal.list","deal.create","company.search"],
    cmds:["hubspot-cli contacts list --limit 10","hubspot-cli contacts search --email john@example.com","hubspot-cli deals create --name 'Enterprise Deal' --amount 50000 --stage appointmentscheduled","hubspot-cli companies search --domain acme.com"],
    plat:["linux","macos","windows"],req:["hubspot-api-key"],inf:["json"],outf:["json"]},

  {n:"salesforce",v:"1.0.0",d:"Salesforce CRM operations. SOQL queries, record CRUD on any sObject, schema exploration.",ld:"CLI for Salesforce REST API. Execute SOQL queries, perform CRUD operations on any sObject (Account, Contact, Lead, Opportunity), and explore object schemas. Supports OAuth2 and access token auth.",c:"cloud",t:["crm","enterprise","salesforce"],dl:"3.1K",ts:134,logo:S+"salesforce/00A1E0",q:.91,
    caps:["query.soql","record.get","record.create","record.update","record.delete","objects.list"],
    cmds:["salesforce-cli query 'SELECT Id, Name FROM Account LIMIT 10'","salesforce-cli record create Contact --data '{\"FirstName\":\"Jane\",\"LastName\":\"Doe\"}'","salesforce-cli record get Account 001xx000003ABCDEF","salesforce-cli objects list"],
    plat:["linux","macos","windows"],req:["salesforce-credentials"],inf:["json"],outf:["json"]},

  {n:"shopify",v:"1.0.0",d:"Shopify e-commerce management. Products, orders, customers, and inventory operations.",ld:"CLI for Shopify Admin REST API. Manage products (list, create, update), orders (list, get), customers (list, search), and inventory levels. Full JSON output for agent workflows.",c:"cloud",t:["ecommerce","shopify","retail"],dl:"2.6K",ts:112,logo:S+"shopify/7AB55C",q:.89,
    caps:["product.list","product.create","product.update","order.list","order.get","customer.list","inventory.list"],
    cmds:["shopify-cli products list --limit 10 --status active","shopify-cli products create --title 'New T-Shirt' --price 29.99 --sku 'TSH-001'","shopify-cli orders list --limit 5 --status any","shopify-cli customers list --limit 10"],
    plat:["linux","macos","windows"],req:["shopify-access-token"],inf:["json"],outf:["json"]},

  {n:"stripe",v:"1.0.0",d:"Stripe payment API. Customers, payment intents, subscriptions, refunds, and product management.",ld:"CLI for Stripe payment API. Manage customers, create and confirm payment intents, handle subscriptions and refunds, and manage products with pricing. Built on Stripe Python SDK with JSON output.",c:"cloud",t:["payments","fintech","stripe"],dl:"3.8K",ts:156,logo:S+"stripe/635BFF",q:.92,
    caps:["customer.manage","payment.create","payment.confirm","subscription.manage","refund.create","product.create"],
    cmds:["stripe-cli customer create --email customer@example.com --name 'Jane Doe'","stripe-cli payment create --amount 5000 --currency usd --customer cus_xxx","stripe-cli subscription list --customer cus_xxx --status active","stripe-cli refund create --payment-intent-id pi_xxx --amount 1000"],
    plat:["linux","macos","windows"],req:["stripe-api-key"],inf:["json"],outf:["json"]},

  {n:"vercel",v:"1.0.0",d:"Vercel deployment platform. Manage deployments, projects, domains, and environment variables.",ld:"CLI for Vercel REST API. List and inspect deployments, manage projects and domains, configure environment variables. Supports team scope and provides JSON output for agent integration.",c:"cloud",t:["deployment","hosting","vercel"],dl:"3.2K",ts:123,logo:S+"vercel/000000",q:.90,
    caps:["deployment.list","deployment.get","deployment.cancel","project.list","domain.list","env.manage"],
    cmds:["vercel-cli deployments list --project my-app --limit 10","vercel-cli deployments get dpl_xxxxx","vercel-cli projects list --limit 20","vercel-cli env add --project my-app --key API_URL --value https://api.example.com --target production"],
    plat:["linux","macos","windows"],req:["vercel-token"],inf:["json"],outf:["json"]},

  // ── Media / Entertainment ──
  {n:"spotify",v:"1.0.0",d:"Spotify music streaming. Search tracks, manage playlists, control playback, get recommendations.",ld:"Spotify Web API wrapper. Search music, manage playlists, control playback, get artist info, and generate recommendations.",c:"media",t:["music","streaming","api"],dl:"5.4K",ts:167,logo:S+"spotify/1DB954",q:.93,
    caps:["track.search","playlist.create","playlist.manage","playback.control","artist.info","recommend.get"],
    cmds:["spotify-cli search 'bohemian rhapsody' --type track --output json","spotify-cli playlist create --name 'Workout Mix'"],
    plat:["linux","macos","windows"],req:["spotify-api-credentials"],inf:["json"],outf:["json"]},

  {n:"youtube",v:"1.0.0",d:"YouTube video platform. Search videos, manage channels, upload content, retrieve analytics.",ld:"YouTube Data API wrapper. Search videos, manage playlists, upload content, retrieve channel analytics and comments.",c:"media",t:["video","streaming","google"],dl:"6.8K",ts:189,logo:S+"youtube/FF0000",q:.94,
    caps:["video.search","video.upload","playlist.manage","channel.info","comment.list","analytics.get"],
    cmds:["youtube-cli search 'machine learning tutorial' --max-results 10 --output json","youtube-cli upload --file video.mp4 --title 'Demo'"],
    plat:["linux","macos","windows"],req:["google-api-credentials"],inf:["mp4","json"],outf:["json"]},

  {n:"twitch",v:"1.0.0",d:"Twitch live streaming platform. Stream management, chat, clips, channel analytics.",ld:"Twitch API wrapper. Manage streams, read chat, create clips, get channel info, and retrieve viewer analytics.",c:"media",t:["streaming","live","gaming"],dl:"3.1K",ts:134,logo:S+"twitch/9146FF",q:.90,
    caps:["stream.info","chat.read","clip.create","channel.manage","analytics.get","user.info"],
    cmds:["twitch-cli stream info --channel shroud --output json","twitch-cli clips create --channel shroud"],
    plat:["linux","macos","windows"],req:["twitch-api-credentials"],inf:["json"],outf:["json"]},

  {n:"tiktok",v:"1.0.0",d:"TikTok content platform. Video upload, analytics, user management, content discovery.",ld:"TikTok for Business API wrapper. Upload videos, manage content, retrieve analytics, and discover trending content.",c:"media",t:["video","social","tiktok"],dl:"2.8K",ts:98,logo:S+"tiktok/000000",q:.87,
    caps:["video.upload","video.list","analytics.get","user.info","trending.discover"],
    cmds:["tiktok-cli upload --file dance.mp4 --caption 'New dance' --output json","tiktok-cli analytics --days 30"],
    plat:["linux","macos","windows"],req:["tiktok-api-credentials"],inf:["mp4","json"],outf:["json"]},

  {n:"x",v:"1.0.0",d:"X (Twitter) social platform. Post tweets, manage timeline, search, handle DMs and lists.",ld:"X/Twitter API v2 wrapper. Post tweets, read timelines, search content, manage lists, handle direct messages.",c:"media",t:["social","twitter","api"],dl:"4.5K",ts:156,logo:S+"x/000000",q:.92,
    caps:["tweet.post","tweet.search","timeline.read","dm.send","list.manage","user.info"],
    cmds:["x-cli tweet 'Hello from CLI Anything!' --output json","x-cli search 'AI agents' --max 20 --output json"],
    plat:["linux","macos","windows"],req:["x-api-credentials"],inf:["json","txt"],outf:["json"]},

  {n:"vlc",v:"1.0.0",d:"VLC media player automation. Playback control, transcoding, streaming, playlist management.",ld:"Control VLC via CLI and HTTP interface. Play media, transcode formats, set up streaming servers, and manage playlists.",c:"media",t:["media","player","transcode"],dl:"2.1K",ts:112,logo:S+"vlcmediaplayer/FF8800",q:.89,
    caps:["media.play","media.transcode","stream.start","playlist.manage","subtitle.add"],
    cmds:["vlc-cli play video.mp4","vlc-cli transcode --input video.avi --format mp4 --codec h264"],
    plat:["linux","macos","windows"],req:["vlc>=3.0"],inf:["mp4","avi","mkv","mp3","flac"],outf:["mp4","webm","mp3"]},

  // ── Gaming ──
  {n:"steam",v:"1.0.0",d:"Steam gaming platform. Library management, game installation, workshop mods, friend activity.",ld:"Steam Web API and SteamCMD wrapper. Manage game library, install games, download workshop mods, track friend activity.",c:"gaming",t:["games","store","valve"],dl:"4.2K",ts:145,logo:S+"steam/000000",q:.91,
    caps:["game.install","game.list","workshop.download","friend.list","achievement.get","market.search"],
    cmds:["steam-cli library list --output json","steam-cli install --appid 730","steam-cli workshop download --id 123456"],
    plat:["linux","macos","windows"],req:["steamcmd"],inf:["json"],outf:["json"]},

  {n:"minecraft",v:"1.0.0",d:"Minecraft server management. Start/stop servers, manage worlds, plugins, player administration.",ld:"Minecraft server management CLI. Start, stop, configure servers, manage worlds and plugins, handle player whitelist and bans.",c:"gaming",t:["games","server","minecraft"],dl:"3.5K",ts:123,logo:null,q:.89,
    caps:["server.start","server.stop","world.manage","plugin.install","player.manage","backup.create"],
    cmds:["minecraft-cli server start --version 1.20 --memory 4G","minecraft-cli world backup --name survival"],
    plat:["linux","macos","windows"],req:["java>=17"],inf:["json"],outf:["json"]},

  {n:"roblox",v:"1.0.0",d:"Roblox development platform. Publish experiences, manage assets, analytics, moderation.",ld:"Roblox Open Cloud API wrapper. Publish places, manage assets and data stores, retrieve analytics, handle moderation.",c:"gaming",t:["games","development","roblox"],dl:"2.1K",ts:87,logo:null,q:.86,
    caps:["place.publish","asset.upload","datastore.manage","analytics.get","user.info"],
    cmds:["roblox-cli publish --place-id 123 --file game.rbxlx","roblox-cli assets list --output json"],
    plat:["linux","macos","windows"],req:["roblox-api-key"],inf:["rbxlx","json"],outf:["json"]},

  {n:"xbox",v:"1.0.0",d:"Xbox Live platform. Achievements, friends, game clips, profile management.",ld:"Xbox Live API wrapper. Retrieve achievements, manage friends list, access game clips, and view profile information.",c:"gaming",t:["games","xbox","microsoft"],dl:"1.5K",ts:78,logo:S+"xbox/107C10",q:.85,
    caps:["achievement.list","friend.list","clip.list","profile.get","presence.check"],
    cmds:["xbox-cli achievements list --gamertag Player123 --output json","xbox-cli friends list --output json"],
    plat:["linux","macos","windows"],req:["xbox-api-key"],inf:["json"],outf:["json"]},

  {n:"epic",v:"1.0.0",d:"Epic Games Store. Library management, free games tracking, friend activity.",ld:"Epic Games Store API wrapper. Manage game library, track free game offers, view friend activity and achievements.",c:"gaming",t:["games","store","epic"],dl:"1.2K",ts:67,logo:S+"epicgames/313131",q:.84,
    caps:["game.list","free.track","friend.list","achievement.get"],
    cmds:["epic-cli library list --output json","epic-cli free-games --output json"],
    plat:["linux","macos","windows"],req:["epic-api-credentials"],inf:["json"],outf:["json"]},

  {n:"battlenet",v:"1.0.0",d:"Battle.net gaming platform. WoW, Diablo, Overwatch API. Character data, achievements, leaderboards.",ld:"Blizzard Battle.net API wrapper. Access WoW characters, Diablo profiles, Overwatch stats, and game-specific leaderboards.",c:"gaming",t:["games","blizzard","mmo"],dl:"1.8K",ts:89,logo:S+"battledotnet/148EFF",q:.87,
    caps:["wow.character","diablo.profile","overwatch.stats","leaderboard.get","game.info"],
    cmds:["battlenet-cli wow character --realm Illidan --name Arthas --output json"],
    plat:["linux","macos","windows"],req:["battlenet-api-key"],inf:["json"],outf:["json"]},

  {n:"gog",v:"1.0.0",d:"GOG.com gaming platform. DRM-free game library, downloads, user data.",ld:"GOG Galaxy API wrapper. Manage DRM-free game library, download games, access user data and achievements.",c:"gaming",t:["games","drm-free","gog"],dl:"890",ts:56,logo:S+"gogdotcom/86328A",q:.83,
    caps:["game.list","game.download","achievement.get","user.info"],
    cmds:["gog-cli library list --output json","gog-cli download --game-id 123"],
    plat:["linux","macos","windows"],req:["gog-api-token"],inf:["json"],outf:["json"]},

  {n:"chess",v:"1.0.0",d:"Chess.com platform. Player stats, game history, puzzles, leaderboards.",ld:"Chess.com public API wrapper. Retrieve player profiles, game archives, daily puzzles, club info, and leaderboards.",c:"gaming",t:["chess","games","api"],dl:"1.1K",ts:78,logo:S+"chessdotcom/81B64A",q:.86,
    caps:["player.stats","game.archive","puzzle.daily","club.info","leaderboard.get"],
    cmds:["chess-cli player stats --username hikaru --output json","chess-cli puzzle daily --output json"],
    plat:["linux","macos","windows"],req:[],inf:["json"],outf:["json"]},

  {n:"lichess",v:"1.0.0",d:"Lichess open-source chess. Games, puzzles, tournaments, analysis board.",ld:"Lichess API wrapper. Access games, puzzles, tournaments, user profiles, and analysis tools on the open-source chess platform.",c:"gaming",t:["chess","open-source","games"],dl:"780",ts:67,logo:S+"lichess/000000",q:.85,
    caps:["game.list","puzzle.get","tournament.list","user.info","analysis.board"],
    cmds:["lichess-cli games --username DrNykterstein --max 10 --output json"],
    plat:["linux","macos","windows"],req:[],inf:["json"],outf:["json","pgn"]},

  {n:"cs2",v:"1.0.0",d:"Counter-Strike 2 stats. Player profiles, match history, weapon stats, leaderboards.",ld:"CS2 stats API wrapper. Retrieve player profiles, match history, weapon statistics, and competitive leaderboards.",c:"gaming",t:["games","fps","valve"],dl:"1.3K",ts:78,logo:S+"counterstrike/000000",q:.85,
    caps:["player.stats","match.history","weapon.stats","leaderboard.get"],
    cmds:["cs2-cli player stats --steamid 76561198xxxx --output json"],
    plat:["linux","macos","windows"],req:["steam-api-key"],inf:["json"],outf:["json"]},

  {n:"fortnite",v:"1.0.0",d:"Fortnite game stats. Player stats, item shop, news, tournament info.",ld:"Fortnite API wrapper. Retrieve player statistics, current item shop, game news, and tournament information.",c:"gaming",t:["games","battle-royale","epic"],dl:"1.6K",ts:67,logo:null,q:.84,
    caps:["player.stats","shop.items","news.get","tournament.info"],
    cmds:["fortnite-cli stats --player Ninja --output json","fortnite-cli shop --output json"],
    plat:["linux","macos","windows"],req:["fortnite-api-key"],inf:["json"],outf:["json"]},

  {n:"valheim",v:"1.0.0",d:"Valheim dedicated server management. Start/stop, world config, player admin, mod management.",ld:"Valheim dedicated server CLI. Start, stop, and configure servers, manage worlds, handle player administration and mods.",c:"gaming",t:["games","server","survival"],dl:"670",ts:45,logo:null,q:.82,
    caps:["server.start","server.stop","world.config","player.manage","mod.install"],
    cmds:["valheim-cli server start --world MyWorld --port 2456","valheim-cli mods install ValheimPlus"],
    plat:["linux","macos","windows"],req:["steamcmd"],inf:["json"],outf:["json"]},

  {n:"speedrun",v:"1.0.0",d:"Speedrun.com platform. Leaderboards, runs, games, categories, and player records.",ld:"Speedrun.com API wrapper. Browse leaderboards, view submitted runs, search games and categories, track personal bests.",c:"gaming",t:["speedrunning","leaderboards","games"],dl:"450",ts:34,logo:null,q:.81,
    caps:["leaderboard.get","run.list","game.search","category.list","player.records"],
    cmds:["speedrun-cli leaderboard --game sms --category any --output json"],
    plat:["linux","macos","windows"],req:[],inf:["json"],outf:["json"]},

  {n:"hoyoverse",v:"1.0.0",d:"HoYoverse games. Genshin Impact, Star Rail character stats, events, redemption codes.",ld:"HoYoverse API wrapper. Retrieve Genshin Impact and Honkai Star Rail character data, daily check-ins, events, and redeem codes.",c:"gaming",t:["games","gacha","hoyoverse"],dl:"1.4K",ts:67,logo:null,q:.84,
    caps:["character.list","daily.checkin","event.list","code.redeem","stats.get"],
    cmds:["hoyoverse-cli genshin characters --output json","hoyoverse-cli daily checkin"],
    plat:["linux","macos","windows"],req:["hoyoverse-cookie"],inf:["json"],outf:["json"]},

  // ── Image / Design (additions) ──
  {n:"krita",v:"1.0.0",d:"Krita digital painting. Brush engine, layer management, animation, batch export.",ld:"Open-source digital painting application. Script brush operations, manage layers, create frame animations, and batch export.",c:"image",t:["painting","digital-art","open-source"],dl:"1.5K",ts:98,logo:S+"krita/3BABFF",q:.88,
    caps:["image.open","layer.manage","brush.apply","animation.create","export.batch"],
    cmds:["krita-cli export --input painting.kra --format png --dpi 300","krita-cli batch --dir ./art --format webp"],
    plat:["linux","macos","windows"],req:["krita>=5.0"],inf:["kra","png","jpg","tiff"],outf:["png","jpg","webp","tiff"]},

  // ── Developer Tools (additions) ──
  {n:"gitlab",v:"1.0.0",d:"GitLab DevOps platform. Repos, merge requests, CI/CD pipelines, issues, releases.",ld:"GitLab REST API wrapper. Manage repositories, merge requests, CI/CD pipelines, issues, and create releases.",c:"dev",t:["git","ci-cd","devops"],dl:"4.8K",ts:198,logo:S+"gitlab/FC6D26",q:.94,
    caps:["repo.manage","mr.create","pipeline.trigger","issue.create","release.create","runner.manage"],
    cmds:["gitlab-cli mr create --title 'Feature X' --source feature --target main --output json","gitlab-cli pipeline trigger --ref main"],
    plat:["linux","macos","windows"],req:["gitlab-token"],inf:["json"],outf:["json"]},

  {n:"jetbrains",v:"1.0.0",d:"JetBrains IDE automation. Plugin management, project inspection, code formatting, build tools.",ld:"Automate JetBrains IDEs (IntelliJ, PyCharm, WebStorm). Manage plugins, inspect projects, run code analysis, and format code.",c:"dev",t:["ide","jetbrains","development"],dl:"2.8K",ts:134,logo:S+"jetbrains/000000",q:.90,
    caps:["plugin.install","project.inspect","code.format","analysis.run","build.trigger"],
    cmds:["jetbrains-cli plugin install python-community --output json","jetbrains-cli inspect --project ./myapp"],
    plat:["linux","macos","windows"],req:["jetbrains-ide"],inf:["json"],outf:["json"]},

  {n:"obsidian",v:"1.0.0",d:"Obsidian knowledge base. Note creation, search, graph operations, plugin management.",ld:"Obsidian vault management. Create and search notes, manage tags, explore knowledge graph, and handle plugins.",c:"dev",t:["notes","knowledge","markdown"],dl:"2.3K",ts:112,logo:S+"obsidian/7C3AED",q:.89,
    caps:["note.create","note.search","tag.manage","graph.query","plugin.manage","vault.info"],
    cmds:["obsidian-cli create --title 'Meeting Notes' --content '# Agenda' --tags meeting","obsidian-cli search 'project plan'"],
    plat:["linux","macos","windows"],req:["obsidian>=1.0"],inf:["md","json"],outf:["json","md"]},

  {n:"7zip",v:"1.0.0",d:"7-Zip archive management. Compress, extract, list, test archives in 30+ formats.",ld:"7-Zip CLI wrapper. Create and extract archives in 7z, ZIP, TAR, GZIP, and 30+ formats with encryption and split support.",c:"dev",t:["compression","archive","utility"],dl:"3.2K",ts:156,logo:null,q:.92,
    caps:["archive.create","archive.extract","archive.list","archive.test","format.convert"],
    cmds:["7zip-cli compress --input ./folder --output archive.7z --level ultra","7zip-cli extract --input archive.zip --output ./out"],
    plat:["linux","macos","windows"],req:["7zip>=21"],inf:["7z","zip","tar","gz","rar","bz2"],outf:["7z","zip","tar","gz"]},

  // ── AI / ML (additions) ──
  {n:"comfyui",v:"1.0.0",d:"ComfyUI node-based AI image generation. Workflow execution, model management, queue control.",ld:"ComfyUI API wrapper. Execute node-based image generation workflows, manage models, control the generation queue.",c:"ai",t:["generation","nodes","diffusion"],dl:"4.1K",ts:134,logo:null,q:.90,
    caps:["workflow.execute","model.list","queue.manage","image.generate","history.get"],
    cmds:["comfyui-cli run --workflow workflow.json --output ./results","comfyui-cli models list --output json"],
    plat:["linux","macos","windows"],req:["comfyui","python>=3.10"],inf:["json","png"],outf:["png","jpg","webp","json"]},

  {n:"openai",v:"1.0.0",d:"OpenAI API. Chat completions, embeddings, image generation, audio transcription, fine-tuning.",ld:"OpenAI REST API wrapper. Run chat completions (GPT-4), generate embeddings, create images (DALL-E), transcribe audio (Whisper), and manage fine-tuning jobs.",c:"ai",t:["llm","gpt","api"],dl:"8.9K",ts:234,logo:S+"openai/412991",q:.96,
    caps:["chat.complete","embedding.create","image.generate","audio.transcribe","finetune.manage","model.list"],
    cmds:["openai-cli chat 'Explain quantum computing' --model gpt-4o --output json","openai-cli image generate 'a cat in space' --size 1024x1024"],
    plat:["linux","macos","windows"],req:["openai-api-key"],inf:["json","txt","mp3","wav"],outf:["json","png"]},

  // ── Cloud / Infra (additions) ──
  {n:"dropbox",v:"1.0.0",d:"Dropbox cloud storage. File upload/download, sharing, folder management, search.",ld:"Dropbox API wrapper. Upload, download, and share files, manage folders, search content, and handle team operations.",c:"cloud",t:["storage","files","cloud"],dl:"2.8K",ts:123,logo:S+"dropbox/0061FF",q:.90,
    caps:["file.upload","file.download","file.share","folder.manage","search.content"],
    cmds:["dropbox-cli upload --local report.pdf --remote /Reports/report.pdf","dropbox-cli list /Documents --output json"],
    plat:["linux","macos","windows"],req:["dropbox-api-token"],inf:["*"],outf:["json"]},

  {n:"onedrive",v:"1.0.0",d:"Microsoft OneDrive cloud storage. File operations, sharing, sync, search.",ld:"OneDrive/SharePoint API wrapper via Microsoft Graph. Upload, download, share files, manage folders, and search content.",c:"cloud",t:["storage","microsoft","cloud"],dl:"2.4K",ts:112,logo:null,q:.89,
    caps:["file.upload","file.download","file.share","folder.manage","search.content","sync.status"],
    cmds:["onedrive-cli upload --local doc.pdf --remote /Documents/doc.pdf","onedrive-cli list /Documents --output json"],
    plat:["linux","macos","windows"],req:["microsoft-365"],inf:["*"],outf:["json"]},

  {n:"gdrive",v:"1.0.0",d:"Google Drive file management. Upload, download, share, organize, and search files.",ld:"Google Drive API wrapper. Upload, download, share, and organize files. Search by name or content, manage permissions.",c:"cloud",t:["storage","google","cloud"],dl:"3.5K",ts:145,logo:S+"googledrive/4285F4",q:.92,
    caps:["file.upload","file.download","file.share","folder.manage","search.content","permission.set"],
    cmds:["gdrive-cli upload report.pdf --folder 'Shared Reports' --output json","gdrive-cli list --query 'type=pdf' --output json"],
    plat:["linux","macos","windows"],req:["google-api-credentials"],inf:["*"],outf:["json"]},

  {n:"sendgrid",v:"1.0.0",d:"SendGrid email delivery. Send transactional emails, manage templates, track delivery stats.",ld:"SendGrid API wrapper. Send transactional and marketing emails, manage templates, track delivery and engagement statistics.",c:"cloud",t:["email","delivery","api"],dl:"2.1K",ts:98,logo:S+"sendgrid/4A154B",q:.89,
    caps:["email.send","template.manage","stats.get","contact.manage","bounce.list"],
    cmds:["sendgrid-cli send --to user@example.com --subject 'Welcome' --template welcome-template","sendgrid-cli stats --days 30 --output json"],
    plat:["linux","macos","windows"],req:["sendgrid-api-key"],inf:["json","html"],outf:["json"]},

  {n:"mailchimp",v:"1.0.0",d:"Mailchimp email marketing. Campaigns, audiences, templates, automation, analytics.",ld:"Mailchimp API wrapper. Create and send campaigns, manage audiences, design templates, set up automations, and view analytics.",c:"cloud",t:["email","marketing","automation"],dl:"2.5K",ts:112,logo:S+"mailchimp/FFE01B",q:.90,
    caps:["campaign.create","campaign.send","audience.manage","template.list","automation.manage","report.get"],
    cmds:["mailchimp-cli campaign create --subject 'Newsletter' --list-id abc123 --output json","mailchimp-cli audience list --output json"],
    plat:["linux","macos","windows"],req:["mailchimp-api-key"],inf:["json","html"],outf:["json"]},

  {n:"zendesk",v:"1.0.0",d:"Zendesk customer support. Tickets, users, organizations, macros, search.",ld:"Zendesk Support API wrapper. Create and manage tickets, handle users and organizations, apply macros, and search content.",c:"cloud",t:["support","helpdesk","crm"],dl:"2.8K",ts:134,logo:S+"zendesk/03363D",q:.91,
    caps:["ticket.create","ticket.update","ticket.list","user.manage","org.manage","search.content"],
    cmds:["zendesk-cli ticket create --subject 'Bug report' --priority high --output json","zendesk-cli tickets list --status open --output json"],
    plat:["linux","macos","windows"],req:["zendesk-api-credentials"],inf:["json"],outf:["json"]},

  {n:"gads",v:"1.0.0",d:"Google Ads management. Campaigns, ad groups, keywords, reporting, budget control.",ld:"Google Ads API wrapper. Manage campaigns, ad groups, keywords, view performance reports, and control budgets.",c:"cloud",t:["advertising","google","marketing"],dl:"2.1K",ts:98,logo:S+"googleads/4285F4",q:.88,
    caps:["campaign.list","campaign.create","adgroup.manage","keyword.manage","report.generate","budget.set"],
    cmds:["gads-cli campaigns list --output json","gads-cli report --type performance --start 2026-01-01 --end 2026-03-01"],
    plat:["linux","macos","windows"],req:["google-ads-credentials"],inf:["json"],outf:["json","csv"]},

  {n:"gplay",v:"1.0.0",d:"Google Play Console. App management, releases, reviews, performance metrics.",ld:"Google Play Developer API wrapper. Manage apps, create releases, respond to reviews, and track performance metrics.",c:"cloud",t:["mobile","android","google"],dl:"1.8K",ts:87,logo:S+"googleplay/414141",q:.87,
    caps:["app.list","release.create","review.list","review.reply","metrics.get"],
    cmds:["gplay-cli apps list --output json","gplay-cli reviews list --app com.example.app --output json"],
    plat:["linux","macos","windows"],req:["google-play-credentials"],inf:["json","apk","aab"],outf:["json"]},

  // ── Lifestyle / Services ──
  {n:"airbnb",v:"1.0.0",d:"Airbnb listing management. Property listings, reservations, pricing, guest communication.",ld:"Airbnb API wrapper. Manage property listings, handle reservations, adjust pricing, and communicate with guests.",c:"lifestyle",t:["travel","rental","hospitality"],dl:"1.8K",ts:78,logo:S+"airbnb/FF5A5F",q:.86,
    caps:["listing.manage","reservation.list","pricing.set","message.send","review.get"],
    cmds:["airbnb-cli listings list --output json","airbnb-cli reservations --status upcoming --output json"],
    plat:["linux","macos","windows"],req:["airbnb-api-credentials"],inf:["json"],outf:["json"]},

  {n:"booking",v:"1.0.0",d:"Booking.com partner API. Property management, reservations, availability, rates.",ld:"Booking.com Connectivity API wrapper. Manage properties, handle reservations, set availability and rates.",c:"lifestyle",t:["travel","hotel","booking"],dl:"1.2K",ts:67,logo:S+"bookingdotcom/003580",q:.84,
    caps:["property.manage","reservation.list","availability.set","rate.update"],
    cmds:["booking-cli reservations list --from 2026-03-01 --output json","booking-cli availability set --room-id 123 --date 2026-04-01"],
    plat:["linux","macos","windows"],req:["booking-api-credentials"],inf:["json"],outf:["json"]},

  {n:"uber-eats",v:"1.0.0",d:"Uber Eats delivery platform. Store management, orders, menus, delivery tracking.",ld:"Uber Eats API wrapper. Manage restaurant stores, handle orders, update menus, and track delivery status.",c:"lifestyle",t:["food","delivery","restaurant"],dl:"1.5K",ts:67,logo:S+"ubereats/06C167",q:.84,
    caps:["store.manage","order.list","order.accept","menu.update","delivery.track"],
    cmds:["ubereats-cli orders list --status pending --output json","ubereats-cli menu update --store-id abc --file menu.json"],
    plat:["linux","macos","windows"],req:["uber-api-credentials"],inf:["json"],outf:["json"]},

  {n:"doordash",v:"1.0.0",d:"DoorDash delivery platform. Store operations, orders, menu management, delivery logistics.",ld:"DoorDash Drive API wrapper. Manage store operations, handle orders, update menus, and coordinate delivery logistics.",c:"lifestyle",t:["food","delivery","restaurant"],dl:"1.1K",ts:56,logo:S+"doordash/FF3008",q:.83,
    caps:["order.list","order.create","delivery.create","store.info"],
    cmds:["doordash-cli orders list --output json","doordash-cli delivery create --pickup '123 Main St' --dropoff '456 Oak Ave'"],
    plat:["linux","macos","windows"],req:["doordash-api-key"],inf:["json"],outf:["json"]},

  {n:"yelp",v:"1.0.0",d:"Yelp business platform. Business search, reviews, ratings, categories.",ld:"Yelp Fusion API wrapper. Search businesses, read reviews, get ratings, browse categories, and view business details.",c:"lifestyle",t:["reviews","business","local"],dl:"1.8K",ts:89,logo:S+"yelp/D32323",q:.87,
    caps:["business.search","business.details","review.list","category.list","autocomplete.search"],
    cmds:["yelp-cli search 'sushi' --location 'San Francisco' --output json","yelp-cli business get --id north-india-restaurant-sf"],
    plat:["linux","macos","windows"],req:["yelp-api-key"],inf:["json"],outf:["json"]},

  {n:"grab",v:"1.0.0",d:"Grab super-app API. Ride-hailing, food delivery, payments in Southeast Asia.",ld:"Grab API wrapper. Manage ride bookings, food delivery orders, and payment transactions across Southeast Asia.",c:"lifestyle",t:["ride-hailing","food","southeast-asia"],dl:"890",ts:45,logo:S+"grab/00B14F",q:.82,
    caps:["ride.book","ride.status","food.order","payment.process"],
    cmds:["grab-cli ride book --pickup '1.290,103.851' --dropoff '1.300,103.860' --output json"],
    plat:["linux","macos","windows"],req:["grab-api-credentials"],inf:["json"],outf:["json"]},

  {n:"meituan",v:"1.0.0",d:"Meituan platform. Food delivery, hotel booking, local services in China.",ld:"Meituan Open Platform API wrapper. Manage restaurant orders, hotel bookings, and local service listings.",c:"lifestyle",t:["food","delivery","china"],dl:"1.3K",ts:56,logo:null,q:.83,
    caps:["order.list","order.manage","store.info","delivery.track"],
    cmds:["meituan-cli orders list --status new --output json"],
    plat:["linux","macos","windows"],req:["meituan-api-credentials"],inf:["json"],outf:["json"]},

  {n:"eleme",v:"1.0.0",d:"Ele.me food delivery. Restaurant management, orders, menus for China market.",ld:"Ele.me Open Platform API wrapper. Manage restaurant info, handle orders, update menus, and track deliveries.",c:"lifestyle",t:["food","delivery","china"],dl:"980",ts:45,logo:null,q:.82,
    caps:["order.list","order.manage","menu.update","store.info"],
    cmds:["eleme-cli orders list --output json","eleme-cli menu update --store-id 123 --file menu.json"],
    plat:["linux","macos","windows"],req:["eleme-api-credentials"],inf:["json"],outf:["json"]},

  {n:"didi",v:"1.0.0",d:"DiDi ride-hailing platform. Ride management, driver operations, trip analytics.",ld:"DiDi Open Platform API wrapper. Manage ride requests, track trips, and access analytics for China's leading ride platform.",c:"lifestyle",t:["ride-hailing","transport","china"],dl:"1.1K",ts:45,logo:null,q:.82,
    caps:["ride.request","ride.status","trip.history","driver.info"],
    cmds:["didi-cli ride request --pickup '39.9,116.4' --dropoff '39.95,116.45' --output json"],
    plat:["linux","macos","windows"],req:["didi-api-credentials"],inf:["json"],outf:["json"]},

  {n:"kfc",v:"1.0.0",d:"KFC ordering API. Menu browsing, order placement, store locator, promotions.",ld:"KFC delivery/ordering API wrapper. Browse menus, place orders, locate stores, and view current promotions.",c:"lifestyle",t:["food","restaurant","fast-food"],dl:"560",ts:34,logo:null,q:.80,
    caps:["menu.browse","order.place","store.locate","promotion.list"],
    cmds:["kfc-cli menu --store-id 123 --output json","kfc-cli stores near --lat 40.7 --lng -74.0 --output json"],
    plat:["linux","macos","windows"],req:["kfc-api-credentials"],inf:["json"],outf:["json"]},

  {n:"mcdonalds",v:"1.0.0",d:"McDonald's ordering API. Menu, orders, store locator, deals and promotions.",ld:"McDonald's API wrapper. Browse menus, place orders, find nearby stores, and discover current deals and promotions.",c:"lifestyle",t:["food","restaurant","fast-food"],dl:"670",ts:34,logo:null,q:.80,
    caps:["menu.browse","order.place","store.locate","deal.list"],
    cmds:["mcdonalds-cli menu --output json","mcdonalds-cli stores near --lat 40.7 --lng -74.0 --output json"],
    plat:["linux","macos","windows"],req:["mcdonalds-api-credentials"],inf:["json"],outf:["json"]},

  {n:"refine",v:"1.0.0",d:"Refine development framework. CRUD app scaffolding, data provider management, deployment.",ld:"Refine.dev CLI wrapper. Scaffold CRUD applications, manage data providers, configure authentication, and deploy.",c:"dev",t:["framework","crud","react"],dl:"1.2K",ts:67,logo:null,q:.84,
    caps:["project.create","resource.add","provider.configure","build.run","deploy.trigger"],
    cmds:["refine-cli create my-app --preset antd","refine-cli resource add products --output json"],
    plat:["linux","macos","windows"],req:["node>=18"],inf:["json"],outf:["json"]},

  {n:"riot",v:"1.0.0",d:"Riot Games API. League of Legends, Valorant, TFT stats, match history, rankings.",ld:"Riot Games API wrapper. Access League of Legends, Valorant, and TFT player stats, match history, and rankings.",c:"gaming",t:["games","esports","riot"],dl:"1.8K",ts:89,logo:S+"riotgames/D32936",q:.87,
    caps:["summoner.get","match.history","ranking.get","champion.info","valorant.stats"],
    cmds:["riot-cli lol summoner --name Faker --region kr --output json","riot-cli valorant stats --name Player#TAG"],
    plat:["linux","macos","windows"],req:["riot-api-key"],inf:["json"],outf:["json"]},
];

// Helpers
function getPkg(slug){return PACKAGES.find(p=>p.n===slug)}
function getPkgsByCategory(cat){return PACKAGES.filter(p=>p.c===cat)}
function getCatLabel(cat){return CATEGORIES[cat]?.label||cat}
function getCatColor(cat){return CATEGORIES[cat]?.color||'#6366f1'}
function getIconClass(cat){
  const map={image:'img',video:'vid','3d':'d3',office:'ofc',dev:'dev',ai:'ai',comm:'com',database:'db',cloud:'cld',browser:'brw',media:'med',gaming:'gam',lifestyle:'lif'};
  return map[cat]||'dev';
}
