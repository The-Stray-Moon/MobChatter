# Publishing

Each target applies `gradle/target-conventions/publish.gradle`. The shared script publishes the target's Java component to the Sighs Maven repository and derives its Maven coordinates from that target:

```text
groupId:    mod_group_id
artifactId: <mod_name>-<loader>-<minecraft-version>
version:    mod_version
```

A version containing `SNAPSHOT` is sent to `maven-snapshots`; every other version is sent to `maven-releases`. Set credentials only in the publishing shell or CI secret store:

```powershell
$env:SIGHS_PUBLISH_USER = '<username>'
$env:SIGHS_PUBLISH_PASSWORD = '<password>'
```

Build or publish one target from its own directory with the JDK declared in its `ci.properties`:

```powershell
cd targets\fabric-1.20.1
.\gradlew.bat publish
```

The generated POM intentionally omits the target build classpath. Minecraft, loader, mappings, and `common` are packaged or supplied by the runtime rather than exposed as Maven dependencies.

## CurseForge

The CurseForge project ID is `1820068` (`publish_curseforge_project_id` in the root `gradle.properties`). Each target uploads its production artifact with its declared JDK:

```powershell
cd targets\fabric-1.20.1
$env:CURSEFORGE_TOKEN = '<token>'
.\gradlew.bat publishCurseforge
```

`publishCurseforge` needs only the CurseForge project ID and `CURSEFORGE_TOKEN`. The aggregate `publishMods` task uploads to every configured platform, so it additionally requires `publish_modrinth_project_id` and `MODRINTH_TOKEN`.

The release type is `STABLE`, the artifact is the target's `remapJar`/`reobfJar` production jar, and the CurseForge game version and loader are read from that target's properties.

The shared convention script also injects the common resources through the relative path `../../common/src/main/resources`, so every published jar carries the shared assets. For the published artifact it prefers `remapJar` first, then `reobfJar`, and falls back to `jar`.
