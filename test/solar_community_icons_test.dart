import 'package:flutter_test/flutter_test.dart';
import 'package:solar_community_icons/solar_community_icons.dart';

void main() {
  group('existing code points stay stable', () {
    test('first and last icons of the original set', () {
      expect(SolarCommunityLinearIcons.accessibility.codePoint, 0xf101);
      expect(SolarCommunityLinearIcons.zipFile.codePoint, 0xf5e5);
      expect(SolarCommunityBoldIcons.zipFile.codePoint, 0xf5e9);
    });
  });

  group('custom icons', () {
    test('are appended after the original linear glyphs', () {
      expect(SolarCommunityLinearIcons.bee.codePoint, 0xf5e6);
      expect(SolarCommunityLinearIcons.car.codePoint, 0xf5e7);
      expect(SolarCommunityLinearIcons.concreteMixer.codePoint, 0xf5e8);
      expect(SolarCommunityLinearIcons.saw.codePoint, 0xf5e9);
    });

    test('are appended after the original bold glyphs', () {
      expect(SolarCommunityBoldIcons.bee.codePoint, 0xf5ea);
      expect(SolarCommunityBoldIcons.car.codePoint, 0xf5eb);
      expect(SolarCommunityBoldIcons.concreteMixer.codePoint, 0xf5ec);
      expect(SolarCommunityBoldIcons.saw.codePoint, 0xf5ed);
    });

    test('use the package fonts', () {
      expect(
        SolarCommunityLinearIcons.car.fontFamily,
        'SolarCommunityLinearIcons',
      );
      expect(SolarCommunityBoldIcons.car.fontFamily, 'SolarCommunityBoldIcons');
      expect(SolarCommunityBoldIcons.car.fontPackage, 'solar_community_icons');
    });
  });
}
