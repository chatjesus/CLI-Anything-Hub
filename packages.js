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
];

// Helpers
function getPkg(slug){return PACKAGES.find(p=>p.n===slug)}
function getPkgsByCategory(cat){return PACKAGES.filter(p=>p.c===cat)}
function getCatLabel(cat){return CATEGORIES[cat]?.label||cat}
function getCatColor(cat){return CATEGORIES[cat]?.color||'#6366f1'}
function getIconClass(cat){
  const map={image:'img',video:'vid','3d':'d3',office:'ofc',dev:'dev',ai:'ai',comm:'com',database:'db',cloud:'cld',browser:'brw'};
  return map[cat]||'dev';
}
