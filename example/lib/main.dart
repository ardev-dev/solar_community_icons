import 'package:material_ui/material_ui.dart';
import 'package:solar_community_icons/solar_community_icons.dart';

const title = 'solar community icons';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: title,
      home: const MyHomePage(),
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
    );
  }
}

class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text(title)),
      body: Center(
        child: GridView(
          shrinkWrap: true,
          scrollDirection: Axis.vertical,
          padding: const EdgeInsets.all(16),
          gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
            mainAxisSpacing: 16,
            crossAxisSpacing: 16,
            maxCrossAxisExtent: 100,
          ),
          children: const [
            Icon(SolarCommunityLinearIcons.accessibility),
            Icon(SolarCommunityBoldIcons.accumulator),
            Icon(SolarCommunityLinearIcons.addCircle),
            Icon(SolarCommunityBoldIcons.adhesivePlaster),
            Icon(SolarCommunityLinearIcons.airbuds),
            Icon(SolarCommunityBoldIcons.alarm),
            Icon(SolarCommunityLinearIcons.album),
            Icon(SolarCommunityBoldIcons.archive),
            Icon(SolarCommunityLinearIcons.armchair),
            Icon(SolarCommunityBoldIcons.asteroid),
            Icon(SolarCommunityLinearIcons.atom),
            Icon(SolarCommunityBoldIcons.bag),
            Icon(SolarCommunityLinearIcons.windowFrame),
            Icon(SolarCommunityBoldIcons.bookMinimalistic),
            Icon(SolarCommunityLinearIcons.ladle),
            Icon(SolarCommunityBoldIcons.rewind5SecondsBack),
            Icon(SolarCommunityLinearIcons.smartSpeaker2),
            Icon(SolarCommunityBoldIcons.tram),
            Icon(SolarCommunityLinearIcons.usbSquare),
            Icon(SolarCommunityBoldIcons.pills),
            Icon(SolarCommunityLinearIcons.medalStarSquare),
            Icon(SolarCommunityBoldIcons.ovenMitts),
            Icon(SolarCommunityLinearIcons.scanner),
            Icon(SolarCommunityBoldIcons.squareAltArrowUp),
            Icon(SolarCommunityLinearIcons.smartphone),
            Icon(SolarCommunityBoldIcons.teaCup),
            Icon(SolarCommunityLinearIcons.widget2),
            Icon(SolarCommunityBoldIcons.walletMoney),
            Icon(SolarCommunityLinearIcons.running),
            Icon(SolarCommunityBoldIcons.undoLeftRound),
            Icon(SolarCommunityLinearIcons.winrar),
            Icon(SolarCommunityBoldIcons.userPlus),
            Icon(SolarCommunityLinearIcons.shieldKeyhole),
            Icon(SolarCommunityBoldIcons.speaker),
            Icon(SolarCommunityLinearIcons.refreshSquare),
            Icon(SolarCommunityBoldIcons.reciveSquare),
            Icon(SolarCommunityLinearIcons.screencast),
            Icon(SolarCommunityBoldIcons.wirelessCharge),
            Icon(SolarCommunityLinearIcons.starsMinimalistic),
            Icon(SolarCommunityBoldIcons.questionSquare),
            Icon(SolarCommunityLinearIcons.sledgehammer),
            Icon(SolarCommunityBoldIcons.menuDotsCircle2),
            Icon(SolarCommunityLinearIcons.virus),
            Icon(SolarCommunityBoldIcons.pointOnMap),
            Icon(SolarCommunityLinearIcons.galleryDownload),
            Icon(SolarCommunityBoldIcons.playlistMinimalistic3),
            Icon(SolarCommunityLinearIcons.reply2),
            Icon(SolarCommunityBoldIcons.squareBottomUp),
          ],
        ),
      ),
    );
  }
}
