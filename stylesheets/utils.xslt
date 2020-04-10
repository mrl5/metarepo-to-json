<?xml version="1.0" encoding="utf-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" indent="yes" encoding="utf-8" omit-xml-declaration="yes" media-type="string"/>

<xsl:template name="splitter">
   <!--
   https://stackoverflow.com/a/50112577
    -->
    <xsl:param name="remaining-string"/>
    <xsl:param name="pattern"/>
    <xsl:choose>
        <xsl:when test="contains($remaining-string,$pattern)">
            <xsl:text>"</xsl:text>
            <xsl:value-of select="normalize-space(substring-before($remaining-string,$pattern))"/>
            <xsl:text>",</xsl:text>
            <xsl:call-template name="splitter">
                <xsl:with-param name="remaining-string" select="substring-after($remaining-string,$pattern)"/>
                <xsl:with-param name="pattern" select="$pattern"/>
            </xsl:call-template>
        </xsl:when>
        <xsl:otherwise>
            <xsl:text>"</xsl:text>
            <xsl:value-of select="normalize-space($remaining-string)"/>
            <xsl:text>"</xsl:text>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>
