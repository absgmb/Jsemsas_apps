import 'dart:io';

import 'package:flutter/material.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  if (Platform.isAndroid || Platform.isIOS) {
    await MobileAds.instance.initialize();
  }
  runApp(const NovaStreamApp());
}

class NovaStreamApp extends StatelessWidget {
  const NovaStreamApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NovaStream Player',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(useMaterial3: true),
      home: const NovaHomePage(),
    );
  }
}

class NovaHomePage extends StatelessWidget {
  const NovaHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF050507),
      appBar: AppBar(
        title: const Text('NovaStream'),
        backgroundColor: Colors.transparent,
      ),
      body: const SafeArea(
        child: Column(
          children: [
            Expanded(
              child: Center(
                child: Icon(Icons.play_circle_outline, size: 96),
              ),
            ),
            NovaAdRail(),
          ],
        ),
      ),
    );
  }
}

/// Advertising is deliberately outside the media surface. While playback is
/// active this rail should be hidden by the playback controller, so an ad can
/// never pause, seek, cover, or inject audio into a user's media.
class NovaAdRail extends StatefulWidget {
  const NovaAdRail({super.key});

  @override
  State<NovaAdRail> createState() => _NovaAdRailState();
}

class _NovaAdRailState extends State<NovaAdRail> {
  BannerAd? _banner;
  bool _loaded = false;

  // Google test banner IDs. Replace through secure build configuration before
  // production release; never commit production credentials to Git.
  String get _adUnitId {
    if (Platform.isAndroid) return 'ca-app-pub-3940256099942544/6300978111';
    if (Platform.isIOS) return 'ca-app-pub-3940256099942544/2934735716';
    return '';
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (_banner != null || _adUnitId.isEmpty) return;
    _load();
  }

  Future<void> _load() async {
    final width = MediaQuery.sizeOf(context).width.truncate();
    final size = await AdSize.getAnchoredAdaptiveBannerAdSize(
      Orientation.portrait,
      width,
    );
    if (size == null || !mounted) return;

    final banner = BannerAd(
      adUnitId: _adUnitId,
      size: size,
      request: const AdRequest(),
      listener: BannerAdListener(
        onAdLoaded: (ad) {
          if (!mounted) return;
          setState(() {
            _banner = ad as BannerAd;
            _loaded = true;
          });
        },
        onAdFailedToLoad: (ad, _) {
          ad.dispose();
          if (mounted) setState(() => _loaded = false);
        },
      ),
    );
    await banner.load();
  }

  @override
  void dispose() {
    _banner?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!_loaded || _banner == null) return const SizedBox.shrink();
    return AnimatedOpacity(
      opacity: 1,
      duration: const Duration(milliseconds: 180),
      child: SizedBox(
        width: _banner!.size.width.toDouble(),
        height: _banner!.size.height.toDouble(),
        child: AdWidget(ad: _banner!),
      ),
    );
  }
}
