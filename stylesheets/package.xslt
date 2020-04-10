<?xml version="1.0" encoding="utf-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:import href="utils.xslt"/>
<xsl:output method="text" indent="yes" encoding="utf-8" omit-xml-declaration="yes" media-type="string"/>

<xsl:template match="/">
    <xsl:variable name="node" select="eixdump/category/package"/><!-- main node -->
    <xsl:text>{</xsl:text>
    <xsl:text>"name":"</xsl:text>
    <xsl:value-of select="$node/@name"/>
    <xsl:text>"</xsl:text>

    <xsl:text>,"description":"</xsl:text>
    <xsl:value-of select="$node/description"/>
    <xsl:text>"</xsl:text> 

    <xsl:text>,"homepages":[</xsl:text>
    <xsl:call-template name="splitter">
        <xsl:with-param name="remaining-string" select="$node/homepage"/>
        <xsl:with-param name="pattern" select="' '"/>
    </xsl:call-template>
    <xsl:text>]</xsl:text>

    <xsl:text>,"licenses":[</xsl:text>
    <xsl:call-template name="splitter">
        <xsl:with-param name="remaining-string" select="$node/licenses"/>
        <xsl:with-param name="pattern" select="' '"/>
    </xsl:call-template>
    <xsl:text>]</xsl:text>

    <xsl:text>,"versions":[</xsl:text>
    <xsl:for-each select="$node/version">
        <xsl:variable name="v" select="current()/@id"/>
        <xsl:text>{"version":"</xsl:text>
        <xsl:value-of select="$v"/>
        <xsl:text>"</xsl:text>
        <xsl:text>,"cpes":[]}</xsl:text>
        <xsl:if test="position()!=last()">
            <xsl:text>,</xsl:text>
        </xsl:if>
    </xsl:for-each>
    <xsl:text>]</xsl:text>

    <xsl:text>}</xsl:text>
</xsl:template>

</xsl:stylesheet>
